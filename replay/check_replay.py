"""Assert what KaroX sent back after each scripted turn; print step timings.

usage: check_replay.py SCENARIO.json LOG.jsonl AGENT_EXIT_CODE
Exit 1 on any failed expectation.
"""

from __future__ import annotations

import json
import sys

scenario = json.load(open(sys.argv[1], encoding="utf-8"))
requests = [json.loads(line) for line in open(sys.argv[2], encoding="utf-8") if line.strip()]
agent_exit = sys.argv[3] if len(sys.argv) > 3 else "?"
turns = scenario["turns"]
failures: list[str] = []

if not requests:
    print("FAIL: KaroX never reached the model endpoint")
    sys.exit(1)

tools = requests[0]["tools"]
print(f"tools advertised ({len(tools)}): {', '.join(tools)}")
if len(tools) > scenario.get("max_tools", 99):
    failures.append(f"{len(tools)} tools advertised, more than {scenario['max_tools']}")
for name in scenario.get("tools_present", []):
    if name not in tools:
        failures.append(f"tool {name} not advertised")
for name in scenario.get("tools_absent", []):
    if name in tools:
        failures.append(f"tool {name} advertised but should be hidden")

readonly = False
for index, turn in enumerate(turns):
    label = turn.get("note") or (turn.get("tool_calls") or [{}])[0].get("name", "")
    if index + 1 >= len(requests):
        failures.append(f"turn {index} ({label}): run ended before its result came back")
        break
    before = len(requests[index]["messages"])
    new = "\n".join(str(m.get("content") or "") for m in requests[index + 1]["messages"][before:])
    gap = requests[index + 1]["at"] - requests[index]["at"]
    status = "ok"
    if turn.get("readonly_ok") and turn["readonly_ok"] in new:
        readonly = True
        print(f"  turn {index:2} RO   {gap:6.2f}s  {label}: task dir is read-only here; KaroX said so")
        continue
    if turn.get("needs_write") and readonly:
        print(f"  turn {index:2} skip {gap:6.2f}s  {label} (needs a writable task dir)")
        continue
    for needle in turn.get("expect", []):
        if needle not in new:
            status = "FAIL"
            failures.append(f"turn {index} ({label}): expected {needle!r} in the result; got: {new[-600:]!r}")
    for needle in turn.get("expect_absent", []):
        if needle.lower() in new.lower():
            status = "FAIL"
            failures.append(f"turn {index} ({label}): unexpected {needle!r} in the result")
    print(f"  turn {index:2} {status:4} {gap:6.2f}s  {label}")
    print("      | " + new[-400:].replace("\n", "\n      | "))

finishes = len(requests) - len(turns)
print(f"finish attempts: {finishes}; agent exit code: {agent_exit}")
if finishes > scenario.get("max_finishes", 99):
    failures.append(f"finish was refused {finishes - 1} times (loop)")

for failure in failures:
    print("FAIL:", failure)
print("REPLAY", "FAILED" if failures else "PASSED")
sys.exit(1 if failures else 0)
