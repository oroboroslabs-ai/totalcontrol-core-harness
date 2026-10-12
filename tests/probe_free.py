#!/usr/bin/env python3
"""
probe_free.py — verify a TOTALCONTROL CORE (FREE) install end to end.
Run against a running server:  python tests/probe_free.py [base]
"""

import json, sys, urllib.request

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8792"

def rest(path, body=None, method=None, headers=None):
    req = urllib.request.Request(BASE + path,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 method=method or ("POST" if body is not None else "GET"),
                                 headers={"Content-Type": "application/json", **(headers or {})})
    return json.loads(urllib.request.urlopen(req, timeout=60).read())

def main():
    failures = 0
    def mark(name, ok, detail=""):
        nonlocal failures
        print(("  OK " if ok else "  FAIL ") + name + (("  · " + detail) if detail else ""))
        failures += 0 if ok else 1

    h = rest("/api/health")
    mark("health", h.get("ok") is True and h.get("product") == "core-free", h.get("version"))

    m = rest("/api/meta")
    law_ok = (not m.get("extensions")) and "core" == m.get("product")
    mark("core law (no hands surface)", law_ok, m.get("version"))

    b = rest("/api/weights/bodies")
    mark("weight engine alive", "bodies" in b, b.get("engine"))

    doc = rest("/api/doc", {"path": "README.md"})
    mark("doc read", "text" in doc, str(doc.get("size_bytes", 0)) + " bytes")

    tok = (m.get("loop") or {}).get("token", "")
    mem = None
    try:
        mem = rest("/api/memory/put", {"key": "law", "text": "x"})
    except Exception:
        mem = {"error": "denied/absent"}
    mark("stateless law (no memory)", bool(mem.get("error")), str(mem.get("error", ""))[:60])

    job = rest("/api/loop/job", {"model": "verify", "steps": [
        {"tool": "echo", "params": {"check": "core"}},
    ], "token": tok})
    ok1 = job.get("ok") and "job" in job
    if ok1:
        jid = job["job"]["id"]
        rest("/api/loop/run", {"id": jid, "token": tok})
        import time
        st = {}
        for _ in range(30):
            time.sleep(0.4)
            st = rest("/api/loop/status?id=" + jid)
            if st.get("state") == "done":
                break
        ok1 = st.get("state") == "done" and st.get("results", [{}])[0].get("ok")
    mark("loop job cycle", ok1, jid if ok1 else "no job")

    print("\nRESULT: " + ("ALL PASS" if failures == 0 else f"{failures} failure(s)"))
    return 0 if failures == 0 else 1

if __name__ == "__main__":
    sys.exit(main())