#!/usr/bin/env python3
"""
server_core.py — TOTALCONTROL CORE (FREE build)

The simplified, stateless product:
  · static weight core loading (any size · shard blobs; ollama/hf/lmstudio/majors)
  · logical engine (weights retrieved, never embedded)
  · the loop (models only)
  · doc reading, cordis passthrough, orca whitelist
  NO hands, NO extension, NO relay, NO crawler, NO memory — the denials are law,
  not configuration: nothing about hands ships in this package.
Gateway law: 127.0.0.1:8792 only.
"""

import asyncio, sys, time
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

# blackbox law: the engine ships as bytecode only (source stripped). The pyc
# is version-locked to the interpreter that compiled it (CPython 3.13).
_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(_ROOT / "blackbox"))
try:
    import engine  # noqa: E402
except ImportError:
    sys.exit("TOTALCONTROL CORE: core blackbox requires CPython 3.13 — "
             "install Python 3.13.x, rebuild the venv, and relaunch "
             "(see AI-INSTALL.md step 1-2).\n"
             f"current: {sys.version.split()[0]}")

app = FastAPI(title="TotalControl Core — FREE")

ROOT = Path(__file__).resolve().parent
STATE_DIR = ROOT / "sessions"; STATE_DIR.mkdir(exist_ok=True)

BIND = "127.0.0.1"
PORT = 8792

ENGINE = engine.WeightEngine()
LOADED = engine.LoadedWeights(ENGINE, STATE_DIR / "loaded-weights.json")
LOADED.restore()
LOOP = engine.LoopEngine(ENGINE, LOADED)

DENIED = {"memory", "crawl", "hands", "extension", "relay"}


def token_ok(body: dict | None, header_token: str = "") -> bool:
    tok = (body or {}).get("token") or header_token
    return bool(tok) and tok == engine.loop_token()


# ------------------------------------------------------------- loop socket

@app.websocket("/loop")
async def loop_ws(ws: WebSocket):
    await ws.accept()
    await ws.send_json({"kind": "loop-open", "product": "core-free",
                        "tools": engine.LOOP_STEP_TOOLS,
                        "token": engine.loop_token()})
    try:
        while True:
            msg = await ws.receive_json()
            if msg.get("kind") == "ping":
                await ws.send_json({"kind": "pong", "ts": time.time()})
                continue
            if msg.get("kind") == "rpc":
                try:
                    data = await engine.rpc(msg.get("path", ""), msg.get("params") or {},
                                            engine=ENGINE, memory=None, loaded=LOADED,
                                            loop=LOOP, version="3.1-core-free",
                                            bind=f"{BIND}:{PORT}",
                                            relay_info={"hands": False,
                                                        "extensions": 0, "models": 0,
                                                        "intents": 0, "percepts": 0,
                                                        "errors": 0})
                    await ws.send_json({"kind": "rpc", "id": msg.get("id"), "data": data})
                except Exception as e:
                    await ws.send_json({"kind": "rpc-error", "id": msg.get("id"),
                                        "error": str(e)})
    except WebSocketDisconnect:
        pass
    except Exception:
        pass


# ---------------------------------------------------------------- REST

@app.get("/api/health")
async def health():
    return {"ok": True, "service": "totalcontrol-core", "version": "3.1-core-free",
            "product": "core-free", "denied": sorted(DENIED), "ts": time.time()}


@app.get("/api/meta")
async def meta():
    bodies = ENGINE.bodies()
    return {"service": "TotalControl Core Harness", "version": "3.1-core-free",
            "bind": f"{BIND}:{PORT}", "product": "core-free",
            "loop": {"token": engine.loop_token(), "tools": list(engine.LOOP_STEP_TOOLS)},
            "weights": {"bodies": len(bodies.get("bodies", [])),
                        "total_gb_measured": bodies.get("total_gb"),
                        "engine": bodies.get("engine")},
            "memory_records": None,
            "law": ["gateway local-only 127.0.0.1", "loop = models only",
                    "no memory · no crawl · no hands",
                    "weights retrieved — never embedded"]}


@app.get("/api/weights/bodies")
async def weights_bodies():
    return ENGINE.bodies()


@app.get("/api/weights/resolve")
async def weights_resolve(q: str, top_k: int = 8):
    return {"query": q, "hits": ENGINE.search(q, top_k)}


@app.get("/api/weights/verify")
async def weights_verify():
    return ENGINE.verify()


@app.post("/api/weights/load")
async def weights_load_api(body: dict):
    return LOADED.load(body.get("family", "majors"), body.get("path", ""))


@app.get("/api/weights/loaded")
async def weights_loaded_api():
    return LOADED.list()


@app.post("/api/loop/job")
async def loop_job_api(body: dict, x_tc_loop: str = None):
    ok = token_ok(body, x_tc_loop)
    job = LOOP.create(body.get("model", "unknown"), body.get("steps", []), ok)
    if not ok:
        return job
    await LOOP.run(job["job"]["id"], ok)
    return job


@app.post("/api/loop/run")
async def loop_run_api(body: dict, x_tc_loop: str = None):
    return await LOOP.run(body.get("id", ""), token_ok(body, x_tc_loop))


@app.get("/api/loop/status")
async def loop_status_api(id: str):
    return LOOP.status(id)


@app.get("/api/loop/jobs")
async def loop_jobs_api():
    return LOOP.list()


@app.post("/api/doc")
async def api_doc(body: dict):
    return engine.read_doc(body.get("path", ""))


@app.get("/api/cordis/status")
async def cordis_status_api():
    return engine.cordis_status()


@app.post("/api/cordis/call")
async def cordis_call_api(body: dict):
    return engine.cordis_fetch(body.get("path", "/"))


@app.post("/api/orca/call")
async def orca_call_api(body: dict):
    return engine.orca_call(body.get("args", []))


@app.post("/api/wallpaper")
async def wallpaper_set_api(body: dict):
    return engine.wallpaper_set(body)


@app.get("/api/wallpaper")
async def wallpaper_get_api():
    return engine.wallpaper_get()


@app.get("/core")
async def core_gui():
    return FileResponse(ROOT / "gui-core" / "index.html")


app.mount("/gui", StaticFiles(directory=ROOT / "gui-core"), name="gui")

# hands assets are not shipped: /hands, /relay, /ext do not exist here.
@app.get("/hands")
async def hands_removed():
    return JSONResponse({"error": "hands is the paid product — not part of TotalControl Core (free)"},
                        status_code=404)

if __name__ == "__main__":
    uvicorn.run(app, host=BIND, port=PORT)