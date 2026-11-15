"""KaroX 6 replay extras: the event stream ends in run_finished with the expected
status, and the finish snapshot holds the expected files.

usage: check_karox6.py SCENARIO.json OUT_DIR   (exit 1 on any failure)
"""

from __future__ import annotations

import glob
import json
import os
import sys

scenario = json.load(open(sys.argv[1], encoding="utf-8"))
out = sys.argv[2]
failures: list[str] = []
events = []
for line in open(os.path.join(out, "events.jsonl"), encoding="utf-8", errors="replace"):
    try:
        events.append(json.loads(line))
    except ValueError:
        failures.append(f"non-JSON line on stdout: {line[:120]!r}")
if not events or events[-1].get("type") != "run_finished":
    failures.append("event stream does not end with run_finished")
else:
    done = events[-1]
    print(f"run_finished: status={done.get('status')} steps={done.get('steps')} "
          f"files_changed={done.get('files_changed')} reason={done.get('reason')!r}")
    if done.get("status") != scenario.get("expect_status", "completed"):
        failures.append(f"status {done.get('status')!r}, expected {scenario.get('expect_status')!r}")
    if events[0].get("type") != "run_started":
        failures.append("event stream does not start with run_started")
manifests = sorted(glob.glob(os.path.join(out, "karox6", "sessions", "*", "submissions", "*", "manifest.json")))
if scenario.get("expect_snapshot") is not None:
    if not manifests:
        failures.append("no finish snapshot written")
    else:
        manifest = json.load(open(manifests[-1], encoding="utf-8"))
        print(f"snapshot {manifests[-1]}: {sorted(manifest.get('files') or {})}")
        for path in scenario["expect_snapshot"]:
            if not (manifest.get("files") or {}).get(path):
                failures.append(f"snapshot misses {path}")
            elif not os.path.isfile(os.path.join(os.path.dirname(manifests[-1]), "files", path)):
                failures.append(f"snapshot copy of {path} is missing")
for failure in failures:
    print("FAIL:", failure)
print("KAROX6", "FAILED" if failures else "PASSED")
sys.exit(1 if failures else 0)
