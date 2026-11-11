"""HARD12 Harbor adapters for OpenCode V2 (@opencode/cli) and DeepSeek Harness.

Same contract as karo_agent.py: model traffic only through the in-container
loopback relay (127.0.0.1:14000 -> race gateway), the W&B key never enters the
container (only the local gateway key, via env RACE_GATEWAY_KEY), exact pinned
CLI versions, and each CLI driven with the same flags the HARD20 1017 arena used.

    harbor run -a ".../hard12_agents.py:OpenCodeV2@" ...
    harbor run -a ".../hard12_agents.py:DeepSeekHarness@" ...
"""
from __future__ import annotations

import json
import shlex
from typing import override

try:  # inside Harbor (WSL)
    from harbor.agents.installed.base import BaseInstalledAgent
    from harbor.agents.installed.node_install import nvm_node_install_snippet
    from harbor.agents.installed.opencode import OpenCode
    from harbor.environments.base import BaseEnvironment
    from harbor.models.agent.context import AgentContext
except ImportError as exc:  # keep importable for offline tests
    _IMPORT_ERROR = exc

    class BaseInstalledAgent:  # type: ignore[no-redef]
        def __init_subclass__(cls, **kwargs):
            raise ImportError(f"harbor is not importable on this host: {_IMPORT_ERROR}")

    OpenCode = BaseInstalledAgent  # type: ignore[misc,assignment]

GATEWAY_BASE = "http://127.0.0.1:14000/v1"
KEY_ENV = "RACE_GATEWAY_KEY"
OPENCODE_VERSION = "2.2.7"
DSH_VERSION = "0.2.2-rc.1"
NVM = "[ -f ~/.nvm/nvm.sh ] && . ~/.nvm/nvm.sh; "


def opencode_config(alias: str) -> dict:
    """readiness/opencode-config.hard20-1017-max.json with only the endpoint swapped."""
    model = {
        "name": "DeepSeek V4.1 Flash 1017 (HARD12 gateway)",
        "modelID": alias,
        "settings": {"reasoningEffort": "max"},
        "body": {"reasoning_effort": "max"},
        "variants": [{"id": "max", "settings": {"reasoningEffort": "max"},
                      "body": {"reasoning_effort": "max"}}],
        "capabilities": {"reasoning": {"supported": True, "effort": ["max"]}},
    }
    return {
        "$schema": "https://opencode.ai/config.json",
        "model": f"wandb-triad/{alias}",
        "providers": {"wandb-triad": {
            "name": "HARD12 gateway", "env": [KEY_ENV],
            "package": "@opencode/ai/providers/openai-compatible",
            "settings": {"baseURL": GATEWAY_BASE},
            "models": {alias: model},
        }},
    }


def dsh_patch(alias: str) -> str:
    """readiness/hard20-wandb-dsh-1017-max.patch.yml with only the endpoint swapped."""
    return (
        "- id: llm-pi-ai\n  config:\n    providers:\n      wandb-triad:\n"
        f"        apiKeyEnv: {KEY_ENV}\n        api: openai-completions\n"
        f"        baseURL: {GATEWAY_BASE}\n        reasoning: max\n        models:\n"
        f"          - id: {alias}\n            reasoningEfforts:\n              off:\n              max: max\n"
        "- id: agent-default-model\n  config:\n    provider: wandb-triad\n"
        f"    model: {alias}\n    reasoningEffort: max\n"
    )


def _gateway_key(agent) -> str:
    key = (getattr(agent, "_extra_env", None) or {}).get(KEY_ENV, "")
    if not key:
        raise ValueError(f"{KEY_ENV} missing: pass it via agents[].env")
    return key


class OpenCodeV2(OpenCode):
    """Official OpenCode V2 CLI (@opencode/cli) pinned to 2.2.7."""

    ALIAS = "hard12-opencode_v2"

    @staticmethod
    @override
    def name() -> str:
        return "opencode-v2-hard12"

    @override
    def get_version_command(self) -> str | None:
        return NVM + "opencode --version"

    @override
    async def install(self, environment: BaseEnvironment) -> None:
        await self.ensure_system_dependencies(environment, ("curl", "bash", "coreutils"))
        await self.exec_as_agent(environment, command=(
            "set -euo pipefail; " + nvm_node_install_snippet() + " && "
            f"npm i -g @opencode/cli@{OPENCODE_VERSION} && "
            f"opencode --version | grep -q 'v{OPENCODE_VERSION}'"))

    @override
    async def run(self, instruction: str, environment: BaseEnvironment,
                  context: AgentContext) -> None:
        self._instruction = instruction
        config = json.dumps(opencode_config(self.ALIAS))
        env = {KEY_ENV: _gateway_key(self),
               "XDG_CONFIG_HOME": "/tmp/oc-config", "OPENCODE_CONFIG": "/tmp/oc-config/opencode/opencode.json",
               "XDG_DATA_HOME": "/logs/agent/opencode/xdg-data",
               "XDG_STATE_HOME": "/logs/agent/opencode/xdg-state"}
        await self.exec_as_agent(environment, env=env, command=(
            "mkdir -p /tmp/oc-config/opencode && "
            f"printf '%s' {shlex.quote(config)} > /tmp/oc-config/opencode/opencode.json && "
            + NVM +
            # Exactly the arena invocation (hard20_live_one.max_command).
            f"opencode run --standalone --auto --format json --thinking "
            f"--model wandb-triad/{self.ALIAS}#max {shlex.quote(instruction)} "
            "2>&1 </dev/null | stdbuf -oL tee /logs/agent/opencode.txt"))


class DeepSeekHarness(BaseInstalledAgent):
    """Genuine DeepSeek Harness (@deepseek-ai/dsh) pinned to 0.2.2-rc.1."""

    ALIAS = "hard12-deepseek_harness"
    SUPPORTS_ATIF = False

    @staticmethod
    @override
    def name() -> str:
        return "deepseek-harness-hard12"

    @override
    def get_version_command(self) -> str | None:
        return NVM + "dsh --version"

    @override
    async def install(self, environment: BaseEnvironment) -> None:
        await self.ensure_system_dependencies(environment, ("curl", "bash", "coreutils"))
        await self.exec_as_agent(environment, command=(
            "set -euo pipefail; " + nvm_node_install_snippet() + " && "
            f"npm i -g @deepseek-ai/dsh@{DSH_VERSION} && dsh --version"))

    @override
    async def run(self, instruction: str, environment: BaseEnvironment,
                  context: AgentContext) -> None:
        patch = dsh_patch(self.ALIAS)
        env = {KEY_ENV: _gateway_key(self), "DSH_HOME": "/logs/agent/dsh-home"}
        await self.exec_as_agent(environment, env=env, command=(
            "mkdir -p /tmp/dsh && "
            f"printf '%s' {shlex.quote(patch)} > /tmp/dsh/headless.patch.yml && "
            + NVM +
            # Exactly the arena invocation (triad_linux.linux_command + 1017 patch).
            "dsh --profile headless --patch /tmp/dsh/headless.patch.yml --json "
            "--permission-mode workspace-write --approval-policy never "
            f"{shlex.quote(instruction)} 2>&1 </dev/null | stdbuf -oL tee /logs/agent/dsh.jsonl"))

    @override
    def populate_context_post_run(self, context: AgentContext) -> None:
        """Token usage from DSH status/step_end events (as triad_runner.parse_events)."""
        path = self.logs_dir / "dsh.jsonl"
        if not path.exists():
            return
        totals = {"inputTokens": 0, "outputTokens": 0, "cacheReadTokens": 0}
        for line in path.read_text(errors="replace").splitlines():
            try:
                event = json.loads(line)
            except ValueError:
                continue
            if event.get("type") == "status" and event.get("phase") == "step_end":
                for k in totals:
                    v = (event.get("usage") or {}).get(k)
                    if isinstance(v, int):
                        totals[k] += v
        context.n_input_tokens = totals["inputTokens"] + totals["cacheReadTokens"]
        context.n_cache_tokens = totals["cacheReadTokens"]
        context.n_output_tokens = totals["outputTokens"]
