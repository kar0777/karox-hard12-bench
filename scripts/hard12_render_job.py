"""Render the HARD12 Harbor job config: ONE task, the selected arms in parallel.

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
# KaroX 6: the newest karox6-*.whl in wheels/ unless HARD12_KAROX6_WHEEL names one.
_K6 = sorted((RACE / "wheels").glob("karox6-*.whl"),
             key=lambda w: [int(n) for n in re.findall(r"[0-9]+", w.name)])  # dev13 > dev9
WHEEL6 = os.environ.get("HARD12_KAROX6_WHEEL") or (str(_K6[-1]) if _K6 else "")
WRAPUP = 50
# Anthropic lane: a post-run feedback turn per KaroX trial (karox6_agent.interview_command),
# with its own time slice taken from both KaroX arms alike.
INTERVIEW = os.environ.get("UPSTREAM") in ("anthropic", "tokenharbor")
INTERVIEW_S = 120

name, task_path, out = sys.argv[1:4]
task = RACE / name if "/" in name else RACE / "hard12_tasks" / name
timeout = int(float(re.search(r"^\[agent\]\n(?:(?!^\[).*\n)*?timeout_sec\s*=\s*([\d.]+)",
                              (task / "task.toml").read_text(encoding="utf-8"), re.M).group(1)))
opts_file = task / "karo_options.json"
opts = (json.loads(opts_file.read_text(encoding="utf-8")) if opts_file.exists()
        else {"task_dir": "/app", "verify_command": ["python3", "-c", "print('verification ok')"]})
key_env = {"RACE_GATEWAY_KEY": "${RACE_GATEWAY_KEY}"}
# Claude upstreams: KaroX 6 ships with the native Anthropic provider; the adapter hard-codes
# openai-chat, so prepend the native flags unless the arm's flags choose a provider themselves
# (forgetting them on 2026-11-24 ran three A/Bs in a non-shipping configuration).
NATIVE_FLAGS = "--provider anthropic --base-url http://127.0.0.1:14000"


def karox6_flags(env_name: str) -> str:
    flags = os.environ.get(env_name, "").strip()
    if os.environ.get("UPSTREAM") in ("anthropic", "tokenharbor") and "--provider" not in flags:
        flags = f"{NATIVE_FLAGS} {flags}".strip()
    elif "--provider anthropic" in flags and "--base-url" not in flags:
        flags += " --base-url http://127.0.0.1:14000"  # the default /v1 base 404s on /v1/messages
    return flags


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
        # KaroX 6 gets only the task directory: no verification command, no hidden checks.
        {"name": "karox6_agent:KaroX6", "model_name": "hard12-karox6",
         "kwargs": {"wheel_path": WHEEL6, "model_alias": "hard12-karox6",
                    "max_seconds": timeout - WRAPUP - (INTERVIEW_S if INTERVIEW else 0),
                    "task_dir": opts.get("task_dir", "/app"), "interview": INTERVIEW,
                    **({"extra_flags": karox6_flags("HARD12_KAROX6_FLAGS")}
                       if karox6_flags("HARD12_KAROX6_FLAGS") else {})},
         "env": key_env},
        # Second KaroX 6 arm for A/B in the same job: its own wheel and flags, own alias.
        {"name": "karox6_agent:KaroX6B", "model_name": "hard12-karox6b",
         "kwargs": {"wheel_path": os.environ.get("HARD12_KAROX6B_WHEEL") or WHEEL6,
                    "model_alias": "hard12-karox6b",
                    "max_seconds": timeout - WRAPUP - (INTERVIEW_S if INTERVIEW else 0),
                    "task_dir": opts.get("task_dir", "/app"), "interview": INTERVIEW,
                    **({"extra_flags": karox6_flags("HARD12_KAROX6B_FLAGS")}
                       if karox6_flags("HARD12_KAROX6B_FLAGS") else {})},
         "env": key_env},
        {"name": "hard12_agents:OpenCodeV2", "model_name": "wandb-triad/hard12-opencode_v2",
         "kwargs": {}, "env": key_env},
        {"name": "hard12_agents:DeepSeekHarness", "model_name": "hard12-deepseek_harness",
         "kwargs": {}, "env": key_env},
        # Codex CLI through the same gateway (Responses API bridged by litellm); opt-in.
        {"name": "hard12_agents:CodexCli", "model_name": "hard12-codex",
         "kwargs": {}, "env": key_env},
        # Claude Code through the same gateway (Anthropic Messages protocol); opt-in.
        {"name": "hard12_agents:ClaudeCode", "model_name": "hard12-claude_code",
         "kwargs": {}, "env": key_env},
        # Reference solution (task solution/solve.sh): proves a task is solvable on this runner.
        {"name": "oracle", "model_name": "hard12-oracle", "kwargs": {}},
    ],
    "tasks": [{"path": task_path}],
}
all_agents = job["agents"]
job["agents"] = [a for a in all_agents if a["name"] not in ("oracle", "karox6_agent:KaroX6B", "hard12_agents:CodexCli", "hard12_agents:ClaudeCode")]  # opt-in only
job["n_concurrent_trials"] = len(job["agents"])
# HARD12_ARMS (optional, comma list of model aliases' arm names) reruns only
# arms that did not finish (e.g. after a host reboot); default = all arms.
only = [a for a in os.environ.get("HARD12_ARMS", "").split(",") if a]
if only:
    job["agents"] = [a for a in all_agents if a["model_name"].split("/")[-1].removeprefix("hard12-") in only]
    job["n_concurrent_trials"] = len(job["agents"])
# HARD12_ATTEMPTS (optional) = independent repeats per arm (variance runs).
attempts = int(os.environ.get("HARD12_ATTEMPTS", "1"))
if attempts > 1:
    job["n_attempts"] = attempts
    job["n_concurrent_trials"] = len(job["agents"]) * attempts
Path(out).write_text(json.dumps(job, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("rendered", out, "agent_timeout", timeout)
