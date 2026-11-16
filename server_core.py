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
RELEASE = "1.6.0"

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
                                            loop=LOOP, version=RELEASE,
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
    return {"ok": True, "service": "totalcontrol-core", "version": RELEASE,
            "product": "core-free", "agent": True, "tools": True, "skills": True,
            "denied": sorted(DENIED), "ts": time.time()}


@app.get("/api/meta")
async def meta():
    bodies = ENGINE.bodies()
    return {"service": "TotalControl Core Harness", "version": RELEASE,
            "bind": f"{BIND}:{PORT}", "product": "core-free",
            "agent": True, "tools": True, "skills": True,
            "loop": {"token": engine.loop_token(), "tools": list(engine.LOOP_STEP_TOOLS)},
            "weights": {"bodies": len(bodies.get("bodies", [])),
                        "total_gb_measured": bodies.get("total_gb"),
                        "engine": bodies.get("engine")},
            "memory_records": None,
            "law": ["gateway local-only 127.0.0.1", "loop = models only",
                    "agent and skills active on install",
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


FREE_SKILLS = [
    {"name": "static-weight-core", "description": "Load shard headers from Ollama, Hugging Face, LM Studio, and the majors."},
    {"name": "loop", "description": "Models-only loop. Sequential steps stay on this machine."},
    {"name": "doc", "description": "Read a local document."},
    {"name": "cordis", "description": "Cordis passthrough on this machine."},
    {"name": "orca", "description": "Orca whitelist call on this machine."},
]

FREE_TOOLS = {
    "weights.bodies": lambda a: ENGINE.bodies(),
    "weights.resolve": lambda a: {"query": a.get("q", ""), "hits": ENGINE.search(str(a.get("q", "")), int(a.get("top_k", 8) or 8))},
    "weights.verify": lambda a: ENGINE.verify(),
    "weights.load": lambda a: LOADED.load(a.get("family", "majors"), a.get("path", "")),
    "weights.loaded": lambda a: LOADED.list(),
    "doc.read": lambda a: engine.read_doc(a.get("path", "")),
    "cordis.status": lambda a: engine.cordis_status(),
    "cordis.call": lambda a: engine.cordis_fetch(a.get("path", "/")),
    "orca.call": lambda a: engine.orca_call(a.get("args", [])),
    "wallpaper.get": lambda a: engine.wallpaper_get(),
    "wallpaper.set": lambda a: engine.wallpaper_set(a),
}


@app.get("/api/agent/status")
async def agent_status():
    return {"ok": True, "agent": True, "tools": True, "skills": True,
            "permanent": True, "version": RELEASE, "product": "core-free",
            "skill_count": len(FREE_SKILLS), "tool_count": len(FREE_TOOLS),
            "law": "local-only 127.0.0.1",
            "notice": "Agent and skills tools are active on install."}


@app.get("/api/skill/registry")
async def skill_registry():
    return {"ok": True, "skills": FREE_SKILLS, "count": len(FREE_SKILLS), "version": RELEASE}


@app.post("/api/tools/invoke")
async def tools_invoke(body: dict):
    name = str((body or {}).get("tool") or "")
    head = name.split(".", 1)[0]
    if name in DENIED or head in DENIED:
        return {"ok": False, "error": "denied", "tool": name}
    fn = FREE_TOOLS.get(name)
    if not fn:
        return {"ok": False, "error": "unknown tool", "tool": name, "tools": sorted(FREE_TOOLS)}
    try:
        return {"ok": True, "tool": name, "data": fn((body or {}).get("args") or {})}
    except Exception as e:
        return {"ok": False, "tool": name, "error": str(e)}


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