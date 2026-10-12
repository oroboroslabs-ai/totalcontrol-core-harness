# Installing TOTALCONTROL CORE (Free)

This is the install manual for the **free** build of TotalControl Core.
It works in two ways:

- **Human install** — follow the steps in Part A by hand (5 minutes).
- **Assisted install** — give Part B to an AI assistant (Claude, Codex, Copilot,
  any agent with shell access) and let it perform and verify the steps.

The package is portable: everything runs from the folder you unpack it into,
and the gateway is local-only (127.0.0.1). Nothing is sent anywhere.

---

## What ships in the package

| File | What it is |
|---|---|
| `server_core.py` | The free harness server (the panel + the loop) |
| `blackbox/engine.pyc` | The engine, shipped as ready-to-run bytecode |
| `gui-core/` | The control panel (browser UI) |
| `START-CORE.cmd` | One-click launcher for Windows |
| `requirements-core.txt` | The Python dependencies |
| `tests/probe_free.py` | The free-tier verification probe |

Size: about 1.95 MB. Python 3.13 is the required runtime.

---

## Part A — Human install

### Step 1 — Get Python 3.13

TotalControl Core runs on **Python 3.13**.

Check if you have it:

```bat
py -3.13 --version
```

If it prints `Python 3.13.x`, continue. If not, install it:

```bat
winget install -e Python.Python.3.13
```

(or download the installer from [python.org](https://www.python.org/downloads/)
and run it — be sure "Add to PATH" is enabled).

### Step 2 — Download and unpack

Get **TotalControl-Free-Core.zip** from the
[releases page](https://github.com/oroboroslabs-ai/totalcontrol-core-harness/releases/latest)
and unpack it to any folder, for example:

```
C:\TotalControl\TotalControlFreeCore\
```

You do not need an installer. The folder is portable — move it anywhere,
delete it to uninstall.

### Step 3 — Install dependencies

Open PowerShell in the unpacked folder and run:

```bat
py -3.13 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements-core.txt
```

This installs the dependencies (FastAPI, Uvicorn, Pillow, NumPy) into a private
`.venv` inside the folder. Your system Python stays untouched.

### Step 4 — Start

Double-click:

```
START-CORE.cmd
```

(or run `.venv\Scripts\python.exe server_core.py` from the folder).

### Step 5 — Open the panel

Open this address in your browser:

```
http://127.0.0.1:8792/core
```

You should see the **TotalControl Core** panel with the status "core live".

### Step 6 — Load your models and run the loop

1. Press **LOAD STATIC WEIGHT CORE** with the preset of your choice
   (OLLAMA · HUGGINGFACE · LM STUDIO · THE MAJORS).
2. Loaded weight systems appear in the table and report **connected**.
3. Press **VERIFY** to confirm the connected file count.
4. In **THE LOOP · MODELS ONLY**, build a job and press **BUILD · RUN LOOP** —
   the steps execute and results stream back to the panel.

Models are loaded by parsing their file headers only; the heaviest weight
blobs are never embedded in anything — they stay on your disk, in place.

---

## Part B — Give this to an AI assistant

Copy everything in this block to an AI assistant (or point it at raw:

`https://raw.githubusercontent.com/oroboroslabs-ai/totalcontrol-core-harness/main/docs/AI-INSTALL.md`):

```text
You are the installer for TOTALCONTROL CORE (free build) on a Windows machine.
Perform every step in order. Verify after each step. If a step fails, fix it
and retry before moving on. Ask before anything that changes machine settings.

1) Verify Python 3.13: run `py -3.13 --version`. If Python 3.13 is missing,
   install it with `winget install -e Python.Python.3.13`, then re-verify.
   Do not substitute another Python version.

2) In the unpacked package folder, create a virtual environment and install
   the pinned dependencies:
     py -3.13 -m venv .venv
     .venv\Scripts\python.exe -m pip install -r requirements-core.txt
   Verify: `.venv\Scripts\python.exe -c "import fastapi, uvicorn, PIL; print('deps ok')"`

3) Launch: `START-CORE.cmd` (or `.venv\Scripts\python.exe server_core.py`).
   Verify the service answers on http://127.0.0.1:8792/api/health and that
   http://127.0.0.1:8792/core serves the panel.

4) Run the verification probe:
     .venv\Scripts\python.exe tests\probe_free.py
   Report its output to the user.

5) Tell the user how to open http://127.0.0.1:8792/core and press
   LOAD STATIC WEIGHT CORE.

Rules:
- The gateway is local-only (127.0.0.1). Never expose it, tunnel it, or port-forward it.
- Never modify the package contents or the shipped bytecode.
- The package is portable; do not install anything system-wide.
- Playwright is not needed for this package; do not install it.
```

---

## Verification checklist

| Check | Expected |
|---|---|
| `py -3.13 --version` | Python 3.13.x |
| deps import | `deps ok` |
| `http://127.0.0.1:8792/api/health` | service answers, "core live" |
| Panel at `/core` | TotalControl Core panel renders |
| Load a preset | weight systems appear, connected |
| `tests/probe_free.py` | all free-tier probes pass |

---

## Troubleshooting

- **"blackbox requires CPython 3.13"** — the virtual environment was built
  with a different Python. Delete the `.venv` folder and repeat Step 3.
- **Port 8792 already in use** — another TotalControl panel is running.
  Close it, then start again (one panel per machine by design).
- **pip fails behind a proxy** — run pip with your proxy settings:
  `.venv\Scripts\python.exe -m pip install --proxy http://proxy:port -r requirements-core.txt`
- **Antivirus flags the bytecode** — the engine ships as compiled Python
  bytecode; add the folder to your antivirus exclusions if you trust it,
  or inspect the folder before running.
- **Wallpaper change fails** — the path must point to an image file
  (png / jpg / webp / bmp / gif). The panel defaults work without changes.

---

## Uninstall

Close the panel window, then delete the package folder. Nothing was written
outside the folder; the `.venv` is inside it.

---

## Privacy & scope of the free build

- The gateway binds **127.0.0.1 only** — no cloud service, no account, no telemetry.
- Model weights are **retrieved in place — never embedded or copied** into any output.
- The free build has **no memory, no crawler, and no browser hands**.
- The engine ships as ready-to-run compiled bytecode; its source is not included.
- The extended edition (**TotalControl Core Hands**) is in final testing;
  its features are not part of this release. Payments unlock at launch.

---

*TotalControl Core (free) · /A Oroboros / Anthropic · local-only by design*