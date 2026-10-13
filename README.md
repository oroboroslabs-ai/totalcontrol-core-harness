# TOTALCONTROL CORE HARNESS

**Load the static weight core. Hand your installed models their engine.**

The free, simplified, stateless build of the TotalControl harness: loads
weight systems — Ollama, Hugging Face, LM Studio, any path of the majors,
shard blobs of any size (GGUF + safetensors headers parsed directly) — and
runs **the loop**: a models-only data line with sequential tool steps that
stream results back. Runs entirely on your machine; the gateway binds
127.0.0.1 only.

The core technology ships blackboxed — compiled bytecode, no engine source
in this repository. The panel is a total GUI: start and go, no configuration.

## Download

Grab the latest free package from
[Releases](https://github.com/oroboroslabs-ai/totalcontrol-core-harness/releases/latest) —
`TotalControl-Free-Core.zip` — or the direct link:
[`releases/latest/download/TotalControl-Free-Core.zip`](https://github.com/oroboroslabs-ai/totalcontrol-core-harness/releases/latest/download/TotalControl-Free-Core.zip)

Then follow `AI-INSTALL.md` inside the package (a full runbook for an AI
installer) or the human fast path:

```
py -3.13 -m venv .venv
.venv\Scripts\python -m pip install -r requirements-core.txt
START-CORE.cmd
```

Panel: http://127.0.0.1:8792/core → **LOAD STATIC WEIGHT CORE** → VERIFY →
run a loop job. A verification script ships at `tests/probe_free.py`.

## Layout

| path | what |
|---|---|
| `server_core.py` | the free server (127.0.0.1:8792) |
| `blackbox/engine.pyc` | the core technology (bytecode; CPython 3.13 locked) |
| `gui-core/` | the control panel |
| `docs/` | the landing page + runbook copy |
| `tests/probe_free.py` | end-to-end verify |

## TotalControl Core Hands — coming soon

The enhanced build is in final testing; its features are intentionally not
described yet. Payments unlock at launch. This page will host it on release.

## Law

127.0.0.1 only · the loop is models only · no memory, no crawl, no hands in
the free build · weights are retrieved, never embedded · nothing leaves the
machine it runs on.

**TotalControl** — Oroboros Labs. All rights reserved.
## Operations manual (online)

- The full HELP & OPERATIONS MANUAL is hosted on our page: <https://oroboroslabs-ai.github.io/anthropic/operations.html>
- AI installer (this repo): docs/AI-INSTALL.md — raw: <https://raw.githubusercontent.com/oroboroslabs-ai/totalcontrol-core-harness/main/docs/AI-INSTALL.md>

## One-click starters (Q:\\__harness-starters)
- start-oroboros-anthropic-harness-8792.bat — the FULL PAID hands harness (8792: panel + relay + session)
- start-totalcontrol-core-free-8792.bat — the FREE core (8792/core; the free product zip)
- start-oroboros-anthropic-core-harness-8789.bat — the cordis harness set (8789: memory systems + crawlers + doc feed)
The port law: 8792 = one TotalControl server at a time (the paid hands rig or the free core).