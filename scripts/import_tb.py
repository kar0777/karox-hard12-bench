"""Wrap Terminal-Bench 4.x tasks into the HARD12 plumbing (same rules for every arm).

    python3 import_tb.py <set_name> <agent_timeout_s> <task_dir> [<task_dir> ...]

* environment: FROM the task's pinned prebuilt image (+ its WORKDIR) + loopback
  relay entrypoint; the original docker_image pin is moved into the Dockerfile;
* agent phase network = docker bridge allowlist; agent timeout capped (same for all);
* verifier (separate environment, reward.txt) untouched;
* karo_options.json: shell + python approvals (the other CLIs have a full shell).
"""
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from import_external import ENTRY, ENTRYPOINT  # noqa: E402

set_name, cap, dirs = sys.argv[1], float(sys.argv[2]), sys.argv[3:]
listing = ROOT / "data" / "sets" / f"{set_name}.txt"
lines = []
for src in map(Path, dirs):
    out = ROOT / "ext_tasks" / set_name / src.name
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(src, out, ignore=shutil.ignore_patterns("solution"))
    toml = (out / "task.toml").read_text(encoding="utf-8")
    head, sep, env = toml.partition("\n[environment]\n")
    image = re.search(r'^docker_image\s*=\s*"([^"]+)"\s*\n', env, re.M)
    docker_src = (out / "environment" / "Dockerfile").read_text(encoding="utf-8")
    workdir = (re.findall(r"^WORKDIR\s+(\S+)", docker_src, re.M) or ["/app"])[-1]
    base = image.group(1) if image else None
    env = env.replace(image.group(0), "") if image else env
    edir = out / "environment"
    if base:  # build FROM the pinned image instead of rebuilding the recipe
        for p in edir.iterdir():
            if p.is_dir():
                shutil.rmtree(p)
            else:
                p.unlink()
        docker = f"FROM {base}\n"
    else:
        docker = docker_src.rstrip() + "\n"
    shutil.copyfile(ENTRY, edir / "karo_relay.py")
    (edir / "entrypoint.sh").write_text(ENTRYPOINT, encoding="utf-8", newline="\n")
    docker += ("COPY karo_relay.py /opt/karo_relay.py\nCOPY entrypoint.sh /opt/entrypoint.sh\n"
               f"RUN chmod +x /opt/entrypoint.sh\nWORKDIR {workdir}\nENTRYPOINT [\"/opt/entrypoint.sh\"]\n")
    (edir / "Dockerfile").write_text(docker, encoding="utf-8", newline="\n")
    head = re.sub(r"(\[agent\]\s*\ntimeout_sec\s*=\s*)([\d.]+)", lambda m: m.group(1) + str(min(float(m.group(2)), cap)), head)
    head = head.replace("[agent]\n", '[agent]\nnetwork_mode = "allowlist"\nallowed_hosts = ["172.16.0.0/12"]\n', 1)
    env = 'network_mode = "public"\n' + env
    (out / "task.toml").write_text(head + sep + env, encoding="utf-8", newline="\n")
    (out / "karo_options.json").write_text(json.dumps({"task_dir": workdir, "verify_command": [
        ["bash", "-lc", "*"], ["python3", "*"], ["python", "*"]]}, indent=2) + "\n", encoding="utf-8", newline="\n")
    lines.append(f"ext_tasks/{set_name}/{src.name}")
listing.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
print(len(lines), "tasks ->", listing)
