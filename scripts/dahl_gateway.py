"""Write the Dahl gateway config for every Dahl key that is set.

    python3 scripts/dahl_gateway.py <out.yaml>   (prints the env var names it used)

Keys come from DAHL_API_KEY, DAHL_API_KEY_2 .. DAHL_API_KEY_40 (empty ones are skipped).
Each key allows 3 parallel requests (probed 2026-11-21, `parallel_key_limit`, counted per
key), so every alias gets one deployment per key with max_parallel_requests 3 and the
router picks one at random and rests a key that answers 429. The model entries are those of litellm.hard12.dahl2.yaml
(its DAHL_API_KEY deployments), so there is one place that defines them. With DAHL_SLOT/DAHL_SLOTS
(set per job by plan_matrix.py) each job uses only its own subset of the keys. Names only
are printed, never values.
"""

from __future__ import annotations

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "..", "gateway", "litellm.hard12.dahl2.yaml")
NAMES = ["DAHL_API_KEY"] + [f"DAHL_API_KEY_{i}" for i in range(2, 41)]


def main() -> None:
    out = sys.argv[1]
    names = [n for n in NAMES if os.environ.get(n)]
    if not names:
        sys.exit("no Dahl key set")
    # One job of several running at once (plan_matrix.py): take only this job's own keys,
    # so jobs never collide on a key's 3-request limit. More slots than keys: share.
    slots = int(os.environ.get("DAHL_SLOTS") or 0)
    slot = int(os.environ.get("DAHL_SLOT") or 0)
    if slots > 1:
        mine = names[slot % slots :: slots] if slots <= len(names) else [names[slot % len(names)]]
        names = mine or names
    src = open(TEMPLATE, encoding="utf-8").read()
    start = src.index("model_list:\n") + len("model_list:\n")
    end = src.index("litellm_settings:")
    entries = re.findall(r"  - model_name: .*\n(?:    .*\n|      .*\n)+", src[start:end])
    base = [e for e in entries if "os.environ/DAHL_API_KEY\n" in e]
    body = "".join(
        e.replace("os.environ/DAHL_API_KEY\n", f"os.environ/{n}\n") for e in base for n in names
    )
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(src[:start] + body + "\n" + src[end:])
    print(" ".join(names))


if __name__ == "__main__":
    main()
