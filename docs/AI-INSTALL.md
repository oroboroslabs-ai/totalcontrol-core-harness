# AI-INSTALL — TOTALCONTROL CORE (FREE build)

You are the AI installer. Perform every step in order on the user's machine.
Verify after each step. If a step fails, correct it and retry before moving on.
Never send data or open the gateway beyond 127.0.0.1.

## 0) What this package is

TOTALCONTROL CORE — the free, simplified, STATELESS harness:
no hands, no browser extension, no crawler, no memory (law, not config).
It loads the static weight core (any size, shard blobs: Ollama / Hugging Face /
LM Studio / any path) and exposes the LOOP — a models-only data line — plus
doc reading, cordis passthrough, orca whitelist.

Package layout:
  server_core.py      the free server (binds 127.0.0.1:8792)
  blackbox/engine.pyc THE CORE TECHNOLOGY — compiled bytecode (source stripped)
  gui-core/           the control panel (simplified)
  START-CORE.cmd      start and go
  requirements-core.txt

## 1) Environment check (verify)

- **CPython 3.13.x is REQUIRED** — the core blackbox is version-locked
  bytecode. `py -3.13 --version` must print 3.13.x.
- If 3.13 is missing: install Python 3.13 (winget install -e Python.Python.3.13
  or python.org download), then continue. Do not substitute another version.
- Windows + PowerShell available.

## 2) Dependencies

From the package directory:

```
py -3.13 -m venv .venv
.venv\Scripts\python.exe -m pip install --quiet --disable-pip-version-check fastapi uvicorn pillow numpy
```

Verify: `.venv\Scripts\python.exe -c "import fastapi, uvicorn, PIL; print('deps ok')"`
Playwright is NOT needed for this package. Never install it here.

## 3) Launch (start and go)

```
START-CORE.cmd
```
(or: `.venv\Scripts\python.exe server_core.py`)

Verify:
- `curl.exe http://127.0.0.1:8792/api/health` →
  `"service":"totalcontrol-core","version":"3.1-core-free"`
- Open http://127.0.0.1:8792/core → the TOTALCONTROL CORE panel.
- The panel should show "core live".

## 4) Function check (loop)

```
.venv\Scripts\python.exe -c "import json,urllib.request; print(json.loads(urllib.request.urlopen('http://127.0.0.1:8792/api/weights/bodies', timeout=30).read())['engine'])"
```
Expect `weight_access.KnowledgeStorage` or `totalcontrol.builtin-storage`.
Then in the panel:
- Press LOAD STATIC WEIGHT CORE (OLLAMA preset) → systems appear, connected.
- Press VERIFY → files connected count.
- Run BUILD · RUN LOOP → job steps stream back.

## 5) What to tell the user

- The gateway binds 127.0.0.1 only. Nothing leaves this machine.
- Weights are parsed at the header level and RETRIEVED — never embedded.
- No memory, no crawl, no browser hands exist in this product.
- Upgrading hands is the paid package (TotalControl Core Hands) — its
  features are not advertised yet.
- The engine ships as compiled blackbox bytecode; no source is included.

## 6) Troubleshooting

- "core blackbox requires CPython 3.13" → wrong interpreter built the venv;
  delete .venv and rebuild with `py -3.13` per step 2.
- Port 8792 busy → another harness is running. Stop it (close its window)
  and relaunch; the launcher reuses the same port by design.
- `pip` behind a proxy → use `python -m pip install --proxy <user proxy> ...`
- Wallpaper change fails → the image path must be an image file
  (png/jpg/webp/bmp/gif). The panel defaults work without changes.

## 7) Law (never override)

127.0.0.1 only · loop = models only · no memory · no crawl · no hands ·
weights retrieved, never embedded.