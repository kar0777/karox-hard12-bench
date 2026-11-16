"""Wrap DeepSWE v1.1 tasks (datacurve-ai/deep-swe @ 0b9fabb) into the HARD12 plumbing.

    python3 import_deepswe.py <set_name> <agent_timeout_s> <deep-swe>/tasks/<name> [...]

Same rules for every arm:
* environment: FROM the task's pinned prebuilt image + loopback relay entrypoint;
* agent phase network = docker bridge allowlist (the model gateway only), timeout capped;
* verifier untouched (separate environment built from tests/Dockerfile, reward.json);
* the collect hook diffs committed + uncommitted work against the base commit (through a
  temporary index), so an agent that edits files but does not run `git commit` is graded
  on its work (the task text asks for a commit; DeepSWE's own runs used agents that commit);
* solution/ is kept for the oracle arm only (Harbor uploads it for the oracle agent).
"""
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from import_external import ENTRY, ENTRYPOINT  # noqa: E402

def collect(base):
    """Snapshot of committed + uncommitted work vs base, through a temporary index (the
    repository itself is not touched; a failing step leaves no model.patch)."""
    return ("cd /app && git config --global --add safe.directory /app && mkdir -p /logs/artifacts && "
            "cp .git/index /tmp/collect.index && GIT_INDEX_FILE=/tmp/collect.index git add -A && "
            f"GIT_INDEX_FILE=/tmp/collect.index git diff --cached --binary {base} > /logs/artifacts/model.patch")

set_name, cap, dirs = sys.argv[1], float(sys.argv[2]), sys.argv[3:]
listing = ROOT / "data" / "sets" / f"{set_name}.txt"
lines = []
for src in map(Path, dirs):
    out = ROOT / "ext_tasks" / set_name / src.name
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(src, out)
    toml = (out / "task.toml").read_text(encoding="utf-8")
    head, sep, env = toml.partition("\n[environment]\n")
    assert sep, src
    image = re.search(r'^docker_image\s*=\s*"([^"]+)"\s*\n', env, re.M)
    assert image, src
    env = env.replace(image.group(0), "")
    edir = out / "environment"
    for p in edir.iterdir():
        shutil.rmtree(p) if p.is_dir() else p.unlink()
    shutil.copyfile(ENTRY, edir / "karo_relay.py")
    (edir / "entrypoint.sh").write_text(ENTRYPOINT, encoding="utf-8", newline="\n")
    (edir / "Dockerfile").write_text(
        f"FROM {image.group(1)}\nCOPY karo_relay.py /opt/karo_relay.py\n"
        "COPY --chmod=0755 entrypoint.sh /opt/entrypoint.sh\nWORKDIR /app\n"
        'ENTRYPOINT ["/opt/entrypoint.sh"]\n', encoding="utf-8", newline="\n")
    head = re.sub(r"(\[agent\]\s*\nnetwork_mode\s*=\s*)\"no-network\"",
                  r'\1"allowlist"\nallowed_hosts = ["172.16.0.0/12"]', head)
    assert 'allowed_hosts = ["172.16.0.0/12"]' in head, src
    agent_at = head.index("[agent]\n")
    head = head[:agent_at] + re.sub(r"^(timeout_sec\s*=\s*)([\d.]+)",
                                    lambda m: m.group(1) + str(min(float(m.group(2)), cap)),
                                    head[agent_at:], count=1, flags=re.M)
    cmd = re.search(r'^\[\[verifier\.collect\]\]\s*\ncommand\s*=\s*"([^"\n]*)"', head, re.M)
    base = re.search(r"git diff --binary ([0-9a-f]{7,40}) HEAD > /logs/artifacts/model\.patch$", cmd.group(1))
    assert base, src
    head = head.replace(cmd.group(1), collect(base.group(1)), 1)
    env = 'network_mode = "public"\n' + env
    (out / "task.toml").write_text(head + sep + env, encoding="utf-8", newline="\n")
    (out / "karo_options.json").write_text(json.dumps({"task_dir": "/app", "verify_command": [
        ["bash", "-lc", "*"], ["python3", "*"], ["python", "*"]]}, indent=2) + "\n",
        encoding="utf-8", newline="\n")
    lines.append(f"ext_tasks/{set_name}/{src.name}")
listing.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
print(len(lines), "tasks ->", listing)
