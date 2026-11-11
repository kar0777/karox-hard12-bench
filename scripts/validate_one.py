"""RED/GREEN validation of ONE fresh candidate on a slim image (GitHub Actions job).

    python3 validate_one.py <candidates.json> <index> <out_dir>

Same objective recipe as the first HARD12 set: python:<ver>-slim + git/build-essential
+ the repo at the fresh base commit (only that commit fetched) + the SWE-rebench
install recipe; Python fallback recipe version -> 3.12 -> 3.13; image cap 3 GiB.
RED = hidden tests on the base commit, GREEN = after the upstream (gold) fix.
Valid: 1..40 fail-to-pass tests and <= 1500 pass-to-pass tests.
Writes <out_dir>/record.json and <out_dir>/Dockerfile.
"""
import json
import re
import shlex
import subprocess
import sys
import time
from pathlib import Path

cands = json.load(open(sys.argv[1], encoding="utf-8"))
c = cands[int(sys.argv[2])]
OUT = Path(sys.argv[3])
OUT.mkdir(parents=True, exist_ok=True)
PYTEST = "python -m pytest --no-header -rA --tb=no --color=no -p no:cacheprovider"


def sh(cmd, timeout=3600):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout,
                          encoding="utf-8", errors="replace")


def parse(log):
    return {m.group(2): m.group(1) for m in
            re.finditer(r"^(PASSED|FAILED|ERROR|XFAIL|XPASS|SKIPPED)\s+(\S+)", log, re.M)}


def dockerfile(ver):
    cfg = c["install_config"]
    install = cfg.get("install") or "pip install -e ."
    pre = " && ".join(x for x in (cfg.get("pre_install") or []) if isinstance(x, str))
    extra = " ".join(shlex.quote(p) for p in (cfg.get("pip_packages") or []) if isinstance(p, str))
    steps = [f"cd /testbed && {install}", "pip install --quiet pytest"]
    if extra:
        steps.insert(0, f"pip install --quiet {extra}")
    return f"""FROM python:{ver}-slim
RUN apt-get update && apt-get install -y --no-install-recommends git build-essential ca-certificates \\
 && rm -rf /var/lib/apt/lists/*
{('RUN ' + pre) if pre else ''}
RUN git init -q /testbed && cd /testbed \\
 && git fetch -q --depth=1 https://github.com/{c['repo']}.git {c['base']} \\
 && git checkout -q -B hard12-base FETCH_HEAD && git remote | xargs -r -n1 git remote remove
RUN {' && '.join(steps)}
WORKDIR /testbed
"""


key = f"{c['repo']}#{c['pr']}"
rec = {"key": key, "repo": c["repo"], "pr": c["pr"], "valid": False}
tag, name = "h12val:latest", "h12val"
t0 = time.time()
try:
    ctx = OUT / "ctx"
    ctx.mkdir(exist_ok=True)
    first = str(c["install_config"].get("python") or "3.11")
    for ver in dict.fromkeys([first, "3.12", "3.13"]):
        (ctx / "Dockerfile").write_text(dockerfile(ver), encoding="utf-8")
        b = sh(f"docker build -q -t {tag} {shlex.quote(str(ctx))}", timeout=2400)
        if not b.returncode:
            rec["python"] = ver
            break
    else:
        raise RuntimeError("build failed: " + (b.stderr or b.stdout)[-300:])
    (OUT / "Dockerfile").write_text((ctx / "Dockerfile").read_text(encoding="utf-8"), encoding="utf-8")
    size = sh(f"docker image inspect -f '{{{{.Size}}}}' {tag}").stdout.strip() or "0"
    rec["image_gib"] = round(int(size) / 2**30, 2)
    if rec["image_gib"] > 3.0:
        raise RuntimeError(f"image too large ({rec['image_gib']} GiB > 3 GiB cap)")
    sh(f"docker run -d --name {name} {tag} sleep infinity")
    (OUT / "test.diff").write_text(c["test_patch"], encoding="utf-8")
    (OUT / "gold.diff").write_text(c["gold_patch"], encoding="utf-8")
    sh(f"docker cp {OUT / 'test.diff'} {name}:/tmp/test.diff")
    sh(f"docker cp {OUT / 'gold.diff'} {name}:/tmp/gold.diff")
    files = sorted({l.split()[2][2:] for l in c["test_patch"].splitlines()
                    if l.startswith("diff --git ") and l.split()[2].endswith(".py")})
    if not files:
        raise RuntimeError("no python test files")

    def dexec(script, timeout=1100):
        return sh(f"docker exec {name} bash -lc {shlex.quote(script)}", timeout=timeout)

    if dexec("cd /testbed && git apply /tmp/test.diff").returncode:
        raise RuntimeError("test patch does not apply")
    run = f"cd /testbed && timeout 900 {PYTEST} {' '.join(shlex.quote(f) for f in files)}"
    red = parse(dexec(run).stdout)
    if dexec("cd /testbed && git apply /tmp/gold.diff").returncode:
        raise RuntimeError("gold patch does not apply")
    green = parse(dexec(run).stdout)
    f2p = sorted(t for t, s in green.items() if s == "PASSED" and red.get(t) != "PASSED")
    p2p = sorted(t for t, s in green.items() if s == "PASSED" and red.get(t) == "PASSED")
    rec.update(test_files=files, f2p=f2p, p2p=p2p,
               green_failures=sorted(t for t, s in green.items() if s in ("FAILED", "ERROR")))
    rec["valid"] = bool(1 <= len(f2p) <= 40 and len(p2p) <= 1500)
    if not rec["valid"]:
        rec["reason"] = "no F2P (env or tests did not run)" if not f2p else "too many tests"
except Exception as exc:  # noqa: BLE001
    rec["reason"] = str(exc)[:400]
rec["seconds"] = round(time.time() - t0)
(OUT / "record.json").write_text(json.dumps(rec) + "\n", encoding="utf-8")
print(("OK  " if rec["valid"] else "BAD ") + key, f"f2p={len(rec.get('f2p', []))}",
      f"img={rec.get('image_gib')}G", rec.get("reason", ""), f"{rec['seconds']}s")
