"""Render the HARD12 Harbor job config: ONE task, THREE arms in parallel.

    python3 hard12_render_job.py <task_name> <wsl_task_path> <out.json>

Same pinned model/gateway/sampling for every arm (gateway profile
inference_profile_hard12.json). Agent wall budget = task [agent] timeout_sec.
"""
import json
import os
import re
import sys
from pathlib import Path

RACE = Path(__file__).resolve().parents[1]
WHEEL = os.environ.get("HARD12_KARO_WHEEL") or str(RACE / "wheels" / "karox_runtime-5.0.0-py3-none-any.whl")
WRAPUP = 50

name, task_path, out = sys.argv[1:4]
task = RACE / name if "/" in name else RACE / "hard12_tasks" / name
timeout = int(float(re.search(r"^\[agent\]\n(?:(?!^\[).*\n)*?timeout_sec\s*=\s*([\d.]+)",
                              (task / "task.toml").read_text(encoding="utf-8"), re.M).group(1)))
opts_file = task / "karo_options.json"
opts = (json.loads(opts_file.read_text(encoding="utf-8")) if opts_file.exists()
        else {"task_dir": "/app", "verify_command": ["python3", "-c", "print('verification ok')"]})
key_env = {"RACE_GATEWAY_KEY": "${RACE_GATEWAY_KEY}"}
job = {
    "n_concurrent_trials": 3,
    "quiet": True,
    "agents": [
        {"name": "karo_agent:Karo", "model_name": "hard12-karox5",
         "kwargs": {"wheel_path": WHEEL, "model_alias": "hard12-karox5",
                    "max_steps": 10000, "max_seconds": timeout - WRAPUP,
                    "effort_level": "ultra", **opts},
         "env": {"KARO_RACE_GATEWAY_URL": "http://127.0.0.1:14000",
                 "KARO_RACE_GATEWAY_KEY": "${RACE_GATEWAY_KEY}"}},
        {"name": "hard12_agents:OpenCodeV2", "model_name": "wandb-triad/hard12-opencode_v2",
         "kwargs": {}, "env": key_env},
        {"name": "hard12_agents:DeepSeekHarness", "model_name": "hard12-deepseek_harness",
         "kwargs": {}, "env": key_env},
    ],
    "tasks": [{"path": task_path}],
}
# HARD12_ARMS (optional, comma list of model aliases' arm names) reruns only
# arms that did not finish (e.g. after a host reboot); default = all three.
only = [a for a in os.environ.get("HARD12_ARMS", "").split(",") if a]
if only:
    job["agents"] = [a for a in job["agents"] if a["model_name"].split("/")[-1].removeprefix("hard12-") in only]
    job["n_concurrent_trials"] = len(job["agents"])
# HARD12_ATTEMPTS (optional) = independent repeats per arm (variance runs).
attempts = int(os.environ.get("HARD12_ATTEMPTS", "1"))
if attempts > 1:
    job["n_attempts"] = attempts
    job["n_concurrent_trials"] = len(job["agents"]) * attempts
Path(out).write_text(json.dumps(job, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("rendered", out, "agent_timeout", timeout)
