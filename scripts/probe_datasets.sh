#!/usr/bin/env bash
curl -LsSf https://astral.sh/uv/install.sh | sh
~/.local/bin/uv tool install --python 3.12 harbor==0.23.0
export PATH=$HOME/.local/bin:$PATH
mkdir -p out
(harbor --help; harbor datasets --help; harbor datasets download --help) > out/help.txt 2>&1 || true
for d in ${DATASETS:-terminal-bench/terminal-bench@4.0.0 datacurve/deep-swe-1-1 swe-rebench/swe-rebench-leaderboard cais/swebenchpro}; do
  n=$(echo "$d" | tr '/@' '__')
  (harbor datasets download "$d" -o "ds/$n" || harbor datasets download "$d" --output-dir "ds/$n") > "out/$n.log" 2>&1 || true
done
python3 - <<'EOF'
import os, json, glob, re
rep = {}
for ds in sorted(glob.glob("ds/*")):
    tasks = [os.path.dirname(p) for p in glob.glob(f"{ds}/**/task.toml", recursive=True)]
    info = {"n": len(tasks), "samples": []}
    for t in tasks[:400]:
        toml = open(f"{t}/task.toml").read()
        env = sorted(os.listdir(f"{t}/environment")) if os.path.isdir(f"{t}/environment") else []
        info["samples"].append({"task": os.path.relpath(t, ds), "env": env[:8],
            "toml": {k: v for k, v in re.findall(r'^(\w+)\s*=\s*(.+)$', toml, re.M) if k in (
                "difficulty", "category", "created_at", "allow_internet", "network", "cpus", "memory", "memory_mb",
                "timeout_sec", "storage_mb", "gpus", "docker_image", "source", "tags")}})
    rep[ds] = info
json.dump(rep, open("out/datasets.json", "w"), indent=1)
print({k: v["n"] for k, v in rep.items()})
EOF
tar czf out/sample_tasks.tgz $(for ds in ds/*; do find "$ds" -name task.toml | head -3 | xargs -n1 dirname; done) 2>/dev/null || true
if [ -n "$FULL_TAR" ]; then tar czf out/full_tasks.tgz ds; fi
