"""Wrap Harbor-hub tasks (SWE-rebench leaderboard, ...) into the HARD12 plumbing.

    python3 import_external.py <set_name> <task_dir> [<task_dir> ...]

Identical for every arm, nothing derived from the hidden tests:
* environment: the task's own Dockerfile + the repo stripped to HEAD's history
  (no future commits/refs to copy a fix from) + the loopback relay entrypoint;
  the repo's conda env (the one the task's test.sh activates) is put on PATH;
* task.toml: agent phase network = docker bridge allowlist (no internet),
  agent timeout capped at 3600 s; verifier and grading untouched (reward.txt);
* karo_options.json: generic "pytest / python" approvals only.
Writes ext_tasks/<set_name>/<task>/ and appends the paths to data/sets/<set_name>.txt.
"""
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENTRY = (ROOT / "hard12_tasks" / "_plumbing" / "karo_relay.py")
ENTRYPOINT = """#!/bin/bash
GW=$(python3 -c "r = open('/proc/net/route').read().splitlines(); l = [x.split() for x in r if x.split() and x.split()[1] == '00000000'][0]; print('.'.join(str(int(l[2][i:i+2], 16)) for i in (6, 4, 2, 0)))" 2>/dev/null || /opt/conda/bin/python -c "r = open('/proc/net/route').read().splitlines(); l = [x.split() for x in r if x.split() and x.split()[1] == '00000000'][0]; print('.'.join(str(int(l[2][i:i+2], 16)) for i in (6, 4, 2, 0)))")
PY=$(command -v /opt/conda/bin/python || command -v python3)
"$PY" /opt/karo_relay.py 14000 "$GW:4110" >/tmp/relay_llm.log 2>&1 &
exec "$@"
"""


def main() -> None:
    set_name, dirs = sys.argv[1], sys.argv[2:]
    out_root = ROOT / "ext_tasks" / set_name
    listing = ROOT / "data" / "sets" / f"{set_name}.txt"
    listing.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    for src in map(Path, dirs):
        name = src.name.lower().replace("_", "-")[:60]
        out = out_root / name
        if out.exists():
            shutil.rmtree(out)
        shutil.copytree(src, out, ignore=shutil.ignore_patterns("solution"))
        test_sh = (out / "tests" / "test.sh").read_text(encoding="utf-8", errors="replace")
        envs = list(dict.fromkeys(re.findall(r"envs/([A-Za-z0-9_.-]+)/bin", test_sh))) or ["testbed"]
        path = ":".join(f"{root}/envs/{e}/bin" for e in envs[:1] for root in ("/opt/conda", "/opt/miniconda3"))
        env = out / "environment"
        shutil.copyfile(ENTRY, env / "karo_relay.py")
        (env / "entrypoint.sh").write_text(ENTRYPOINT, encoding="utf-8", newline="\n")
        docker = (env / "Dockerfile").read_text(encoding="utf-8").rstrip() + "\n"
        docker += f"""RUN cd /testbed \\
 && git config --global --add safe.directory /testbed \\
 && (git remote | xargs -r -n1 git remote remove) \\
 && git branch -f hard12-base HEAD 2>/dev/null; git checkout -q hard12-base 2>/dev/null; \\
 (git for-each-ref --format='%(refname)' | grep -v '^refs/heads/hard12-base$' | xargs -r -n1 git update-ref -d) \\
 && git reflog expire --expire=now --all && git gc --prune=now -q
ENV PATH={path}:$PATH
COPY karo_relay.py /opt/karo_relay.py
COPY entrypoint.sh /opt/entrypoint.sh
RUN chmod +x /opt/entrypoint.sh
WORKDIR /testbed
ENTRYPOINT ["/opt/entrypoint.sh"]
"""
        (env / "Dockerfile").write_text(docker, encoding="utf-8", newline="\n")
        toml = (out / "task.toml").read_text(encoding="utf-8")
        toml = re.sub(r"(\[agent\]\s*\ntimeout_sec\s*=\s*)([\d.]+)",
                      lambda m: m.group(1) + str(min(float(m.group(2)), 3600.0)), toml)
        toml = toml.replace("[agent]\n", '[agent]\nnetwork_mode = "allowlist"\nallowed_hosts = ["172.16.0.0/12"]\n', 1)
        toml = toml.replace("[environment]\n", '[environment]\nnetwork_mode = "public"\n', 1)
        (out / "task.toml").write_text(toml, encoding="utf-8", newline="\n")
        (out / "karo_options.json").write_text(json.dumps(
            {"task_dir": "/testbed", "verify_command": [["python", "-m", "pytest", "*"], ["python", "*"]]},
            indent=2) + "\n", encoding="utf-8", newline="\n")
        lines.append(f"ext_tasks/{set_name}/{name}")
    listing.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(len(lines), "tasks ->", listing)


if __name__ == "__main__":
    main()
