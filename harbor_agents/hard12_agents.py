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
OPENCODE_VERSION = "2.3.2"
DSH_VERSION = "0.2.2-rc.5"
CODEX_VERSION = "0.171.0"
CLAUDE_CODE_VERSION = "2.1.329"
PLAYWRIGHT_MCP_VERSION = "0.0.41"  # official Microsoft browser MCP, used on web-task images only
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
    """Official OpenCode V2 CLI (@opencode/cli) pinned to 2.3.2."""

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
            f"opencode --version | grep -q 'v{OPENCODE_VERSION}' && "
            # Web-task images ship Chromium: give OpenCode the official Playwright MCP.
            f"if [ -x /usr/local/bin/chromium-pw ]; then npm i -g @playwright/mcp@{PLAYWRIGHT_MCP_VERSION}; fi"))

    @override
    async def run(self, instruction: str, environment: BaseEnvironment,
                  context: AgentContext) -> None:
        self._instruction = instruction
        config = opencode_config(self.ALIAS)
        web = json.dumps(dict(config, mcp={"playwright": {"type": "local", "enabled": True, "command": [
            "mcp-server-playwright", "--headless", "--no-sandbox", "--isolated",
            "--executable-path", "/usr/local/bin/chromium-pw"]}}))
        config = json.dumps(config)
        env = {KEY_ENV: _gateway_key(self),
               "XDG_CONFIG_HOME": "/tmp/oc-config", "OPENCODE_CONFIG": "/tmp/oc-config/opencode/opencode.json",
               "XDG_DATA_HOME": "/logs/agent/opencode/xdg-data",
               "XDG_STATE_HOME": "/logs/agent/opencode/xdg-state"}
        await self.exec_as_agent(environment, env=env, command=(
            "mkdir -p /tmp/oc-config/opencode && "
            f"printf '%s' {shlex.quote(config)} > /tmp/oc-config/opencode/opencode.json && "
            f"if [ -x /usr/local/bin/chromium-pw ]; then printf '%s' {shlex.quote(web)} "
            "> /tmp/oc-config/opencode/opencode.json; fi && "
            + NVM +
            # Exactly the arena invocation (hard20_live_one.max_command).
            f"opencode run --standalone --auto --format json --thinking "
            f"--model wandb-triad/{self.ALIAS}#max {shlex.quote(instruction)} "
            "2>&1 </dev/null | stdbuf -oL tee /logs/agent/opencode.txt"))


class DeepSeekHarness(BaseInstalledAgent):
    """Genuine DeepSeek Harness (@deepseek-ai/dsh) pinned to 0.2.2-rc.5."""

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


def codex_config(alias: str) -> str:
    """Codex config.toml: the gateway as a custom provider (Responses API)."""
    lines = [
        f'model = "{alias}"',
        'model_provider = "hard12"',
        # The alias is not a model Codex knows: without this it falls back to default
        # metadata (a smaller window). The lanes serve a 1M-token window (gateway model_info).
        "model_context_window = 1048576",
        'model_reasoning_effort = "high"',
        'approval_policy = "never"',
        'sandbox_mode = "danger-full-access"',
        "[model_providers.hard12]",
        'name = "HARD12 gateway"',
        f'base_url = "{GATEWAY_BASE}"',
        f'env_key = "{KEY_ENV}"',
        'wire_api = "responses"',
    ]
    return "\n".join(lines) + "\n"


class CodexCli(BaseInstalledAgent):
    """OpenAI Codex CLI (@openai/codex) pinned, driven through the same gateway alias
    scheme as the other arms. The gateway enforces the sampling profile (effort included)."""

    ALIAS = "hard12-codex"
    SUPPORTS_ATIF = False

    @staticmethod
    @override
    def name() -> str:
        return "codex-hard12"

    @override
    def get_version_command(self) -> str | None:
        return NVM + "codex --version"

    @override
    async def install(self, environment: BaseEnvironment) -> None:
        await self.ensure_system_dependencies(environment, ("curl", "bash", "coreutils"))
        await self.exec_as_agent(environment, command=(
            "set -euo pipefail; " + nvm_node_install_snippet() + " && "
            f"npm i -g @openai/codex@{CODEX_VERSION} && codex --version"))

    @override
    async def run(self, instruction: str, environment: BaseEnvironment,
                  context: AgentContext) -> None:
        # CODEX_HOME stays outside /logs: Codex keeps files only root may read there
        # (tmp/arg0-*), Harbor walks every file of the trial directory as the runner's user
        # and the artifact upload does the same (devc0: PermissionError, no artifact). Not
        # under /tmp either: Codex refuses to put its helper binaries (the apply_patch
        # alias) into a temporary directory (devc1). The session files and logs are copied
        # out afterwards, readable.
        env = {KEY_ENV: _gateway_key(self)}
        config = shlex.quote(codex_config(self.ALIAS))
        await self.exec_as_agent(environment, env=env, command=(
            'export CODEX_HOME="${HOME:-/opt}/.codex-hard12" && mkdir -p "$CODEX_HOME" && '
            f"printf '%s' {config} > \"$CODEX_HOME/config.toml\" && "
            + NVM +
            "codex exec --dangerously-bypass-approvals-and-sandbox --skip-git-repo-check --json "
            f"-- {shlex.quote(instruction)} 2>&1 </dev/null | stdbuf -oL tee /logs/agent/codex.jsonl; "
            "mkdir -p /logs/agent/codex-home; "
            'cp -r "$CODEX_HOME/sessions" "$CODEX_HOME/log" /logs/agent/codex-home/ 2>/dev/null; '
            "chmod -R a+rX /logs/agent/codex-home /logs/agent/codex.jsonl 2>/dev/null; true"))


class ClaudeCode(BaseInstalledAgent):
    """Anthropic Claude Code (@anthropic-ai/claude-code) pinned, headless, through the same
    gateway on the Anthropic Messages protocol (litellm /v1/messages, no format
    translation). Every model role (main, small/fast) uses the one race alias."""

    ALIAS = "claude-haiku-5-5"  # the real id: Claude Code tunes itself by model name
    SUPPORTS_ATIF = False

    @staticmethod
    @override
    def name() -> str:
        return "claude-code-hard12"

    @override
    def get_version_command(self) -> str | None:
        return NVM + "claude --version"

    @override
    async def install(self, environment: BaseEnvironment) -> None:
        await self.ensure_system_dependencies(environment, ("curl", "bash", "coreutils"))
        await self.exec_as_agent(environment, command=(
            "set -euo pipefail; " + nvm_node_install_snippet() + " && "
            f"npm i -g @anthropic-ai/claude-code@{CLAUDE_CODE_VERSION} && claude --version"))

    @override
    async def run(self, instruction: str, environment: BaseEnvironment,
                  context: AgentContext) -> None:
        env = {
            "ANTHROPIC_BASE_URL": GATEWAY_BASE.removesuffix("/v1"),
            "ANTHROPIC_AUTH_TOKEN": _gateway_key(self),
            "ANTHROPIC_MODEL": self.ALIAS,
            "ANTHROPIC_SMALL_FAST_MODEL": self.ALIAS,
            "ANTHROPIC_DEFAULT_HAIKU_MODEL": self.ALIAS,
            "ANTHROPIC_DEFAULT_SONNET_MODEL": self.ALIAS,
            "ANTHROPIC_DEFAULT_OPUS_MODEL": self.ALIAS,
            "CLAUDE_CODE_SUBAGENT_MODEL": self.ALIAS,
            "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1",
            "DISABLE_AUTOUPDATER": "1",
            "DISABLE_TELEMETRY": "1",
            "IS_SANDBOX": "1",
            "CLAUDE_CONFIG_DIR": "/logs/agent/claude-home",
        }
        await self.exec_as_agent(environment, env=env, command=(
            "mkdir -p /logs/agent/claude-home && " + NVM +
            f"claude -p {shlex.quote(instruction)} --model {self.ALIAS} "
            "--dangerously-skip-permissions --output-format stream-json --verbose "
            "2>&1 </dev/null | stdbuf -oL tee /logs/agent/claude-code.jsonl; "
            "chmod -R a+rX /logs/agent/claude-home /logs/agent/claude-code.jsonl 2>/dev/null; true"))

