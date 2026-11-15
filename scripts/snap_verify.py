"""Grade each submitted-finish snapshot of KaroX trials against the task's hidden tests.

    python3 scripts/snap_verify.py <trial artifact dir> <out dir>

KaroX 5 (v60.21+) and KaroX 6 keep the changed files as they stood at every submitted finish
under <session>/submissions/NN/{files/,manifest.json}. Each snapshot is laid on
a fresh task image (no agent, no model, no key) and graded by the task's own
tests/test.sh, so the first finish can be scored against the final one.
Writes <out dir>/snap_results.jsonl.
"""
import json
import pathlib
import subprocess
import sys

art, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
NAME = "snapv"


def sh(cmd, timeout=1800):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                              encoding="utf-8", errors="replace")
    except subprocess.TimeoutExpired:
        return subprocess.CompletedProcess(cmd, 124, "", "timeout")


rows = []
for trial in sorted(p for p in art.glob("jobs/*/*") if p.is_dir()):
    task = trial.name.split("__")[0]
    task_dir = pathlib.Path("hard12_tasks") / task
    reward_file = trial / "verifier" / "reward.txt"
    final = reward_file.read_text(encoding="utf-8").strip() if reward_file.is_file() else None
    snaps = sorted(trial.glob("agent/karox-runtime/vnext/sessions/*/submissions/*/manifest.json"))
    snaps += sorted(trial.glob("agent/karox6/sessions/*/submissions/*/manifest.json"))  # KaroX 6
    if not task_dir.is_dir() or not snaps:
        rows.append({"task": task, "final_reward": final, "note": "no task dir" if not task_dir.is_dir() else "no snapshots"})
        continue
    image = "snap-" + task.lower()
    built = sh(["docker", "build", "-q", "-t", image, str(task_dir / "environment")], timeout=2400)
    if built.returncode:
        rows.append({"task": task, "final_reward": final, "note": "build failed: " + built.stderr[-300:]})
        continue
    for manifest_path in snaps:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        sh(["docker", "rm", "-f", NAME])
        sh(["docker", "run", "-d", "--name", NAME, "--entrypoint", "sleep", image, "infinity"])
        files = manifest_path.parent / "files"
        if files.is_dir():
            sh(["docker", "cp", f"{files}/.", f"{NAME}:/testbed/"])
        deleted = [path for path, digest in (manifest.get("files") or {}).items() if digest is None]
        if deleted:
            sh(["docker", "exec", NAME, "rm", "-f", "--", *("/testbed/" + path for path in deleted)])
        sh(["docker", "cp", str(task_dir / "tests"), f"{NAME}:/tests"])
        graded = sh(["docker", "exec", NAME, "bash", "/tests/test.sh"], timeout=1500)
        reward = sh(["docker", "exec", NAME, "cat", "/logs/verifier/reward.txt"]).stdout.strip()
        missing = sh(["docker", "exec", NAME, "cat", "/logs/verifier/eval_missing.log"]).stdout.splitlines()
        rows.append({
            "task": task, "submission": manifest.get("index"), "step": manifest.get("step"),
            "files": len(manifest.get("files") or {}), "reward": reward, "missing": len(missing),
            "missing_head": missing[:5], "final_reward": final, "grader_exit": graded.returncode,
        })
        sh(["docker", "rm", "-f", NAME])

with open(out / "snap_results.jsonl", "w", encoding="utf-8") as handle:
    for row in rows:
        handle.write(json.dumps(row) + "\n")
for row in rows:
    print(json.dumps({k: v for k, v in row.items() if k != "missing_head"}))
