"""Append validated candidates as HARD12 tasks 13+ (objective order = order_key).

    python scripts/add_validated_tasks.py <candidates.json> <validation dir with VALIDATION/ and val-<i>/>
"""
import json
import re
import subprocess
import sys

cands_file, vdir = sys.argv[1], sys.argv[2]
cands = json.load(open(cands_file, encoding="utf-8"))
idx = {f"{c['repo']}#{c['pr']}": i for i, c in enumerate(cands)}
recs = [json.loads(l) for l in open(f"{vdir}/VALIDATION/validation.jsonl", encoding="utf-8")]
valid = sorted((r for r in recs if r["valid"]), key=lambda r: cands[idx[r["key"]]]["order_key"])
with open("data/val_new.jsonl", "w", encoding="utf-8", newline="\n") as fh:
    fh.write("".join(json.dumps(r) + "\n" for r in valid))
existing = [l for l in open("data/night_tasks.txt", encoding="utf-8").read().splitlines() if l.strip()]
names = {"h12-" + l.split()[1][:40] for l in existing}
built = 0
with open("data/validation_slim.jsonl", "a", encoding="utf-8", newline="\n") as fv, \
        open("data/night_tasks.txt", "a", encoding="utf-8", newline="\n") as ft:
    for r in valid:
        slug = re.sub(r"[^a-z0-9]+", "-", r["key"].lower()).strip("-")[:50]
        name = "h12-" + slug[:40]
        if name in names:
            print("dup", name)
            continue
        dockerfile = f"{vdir}/val-{idx[r['key']]}/Dockerfile"
        out = subprocess.run([sys.executable, "scripts/make_hard12_task.py", cands_file, "data/val_new.jsonl",
                              r["key"], name, dockerfile], capture_output=True, text=True, encoding="utf-8")
        if out.returncode:
            print("FAIL", r["key"], out.stderr[-300:])
            continue
        names.add(name)
        fv.write(json.dumps(r) + "\n")
        ft.write(f"{r['key']} {slug}\n")
        built += 1
print("built", built)
