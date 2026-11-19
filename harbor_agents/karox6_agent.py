"""Harbor adapter for KaroX 6 (`karox6` wheel), next to karo_agent.py (KaroX 5).

Same contract as hard12_agents.py: model traffic only through the in-container
loopback relay (127.0.0.1:14000 -> race gateway) that the task entrypoint starts;
only the local gateway key enters the container (env RACE_GATEWAY_KEY, read by
KaroX through --api-key-env, never on a command line). Sampling is enforced by
the gateway profile, identical for every arm.

    harbor run -a ".../karox6_agent.py:KaroX6@" ...

KaroX 6 keeps its sessions under /logs/agent/karox6 (collected with the trial):
the JSON event stream is /logs/agent/karox6.jsonl and every run end leaves a
snapshot of the changed files in sessions/<id>/submissions/NN for snapverify.
"""
from __future__ import annotations

import json
import shlex
from pathlib import Path
from typing import Annotated, override

from pydantic import Field

try:  # inside Harbor (WSL / CI)
    from harbor.agents.installed.base import BaseInstalledAgent
    from harbor.agents.options import Cli, InstalledAgentOptions
    from harbor.environments.base import BaseEnvironment
    from harbor.models.agent.context import AgentContext
except ImportError as exc:  # keep importable for offline tests
    _IMPORT_ERROR = exc

    class BaseInstalledAgent:  # type: ignore[no-redef]
        def __init_subclass__(cls, **kwargs):
            raise ImportError(f"harbor is not importable on this host: {_IMPORT_ERROR}")

    class InstalledAgentOptions:  # type: ignore[no-redef]
        pass

    def Cli(*_args, **_kwargs):  # type: ignore[no-redef]  # noqa: N802
        return None


GATEWAY_BASE = "http://127.0.0.1:14000/v1"
KEY_ENV = "RACE_GATEWAY_KEY"
VENV = "/tmp/karox6-venv"
PY = VENV + "/bin/python"
HOME = "/logs/agent/karox6"
EVENTS = "/logs/agent/karox6.jsonl"
STDERR = "/logs/agent/karox6.stderr.txt"

#: A venv for KaroX only (the task's own python stays untouched). KaroX 6 needs
#: Python >= 3.12: older images get a standalone 3.12 through uv. Images without
#: ensurepip get a bare venv plus get-pip.py.
INSTALL = r"""
set -euo pipefail
mkvenv() {
  python3 -m venv "$1" >/dev/null 2>&1 || {
    rm -rf "$1" && python3 -m venv --without-pip "$1" &&
    "$1/bin/python" -c "import urllib.request; exec(urllib.request.urlopen('https://bootstrap.pypa.io/get-pip.py', timeout=120).read())" --quiet
  }
}
if python3 -c 'import sys; sys.exit(sys.version_info < (3, 12))'; then
  mkvenv {venv}
else
  mkvenv /tmp/karox6-uv && /tmp/karox6-uv/bin/python -m pip install --quiet uv &&
  /tmp/karox6-uv/bin/uv venv --quiet --seed --python 3.12 {venv}
fi
{py} -m pip install --quiet --force-reinstall {wheel}
{py} -m karox6 --version
"""


class KaroX6Options(InstalledAgentOptions):
    wheel_path: Annotated[str | None, Cli("--wheel-path")] = Field(
        default=None, description="Host path of the karox6 wheel to install in the container."
    )
    model_alias: Annotated[str, Cli("--model-alias")] = Field(
        default="hard12-karox6", description="Gateway model alias (per-arm accounting)."
    )
    task_dir: Annotated[str | None, Cli("--task-dir")] = Field(
        default="/app", description="Working directory of the task inside the container."
    )
    max_seconds: Annotated[int | None, Cli("--max-seconds")] = Field(
        default=None, description="Wall-clock budget for karox run (task timeout minus wrap-up)."
    )
    max_steps: Annotated[int | None, Cli("--max-steps")] = Field(
        default=None, description="Model-call budget for karox run."
    )
    context_window: Annotated[int, Cli("--context-window")] = Field(
        default=1048576, description="Context window of the served model (gateway model_info)."
    )
    max_output_tokens: Annotated[int, Cli("--max-output-tokens")] = Field(
        default=32768, description="Output token cap (the gateway profile enforces the same)."
    )
    extra_flags: Annotated[str | None, Cli("--extra-flags")] = Field(
        default=None, description="Extra `karox run` flags for A/B arms (shell words)."
    )


class KaroX6(BaseInstalledAgent):
    """Run KaroX 6 headless inside a Harbor task container."""

    options_model = KaroX6Options

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        wheel = getattr(self.options, "wheel_path", None)
        self._wheel_path = Path(wheel) if wheel else None

    @staticmethod
    @override
    def name() -> str:
        return "karox6-hard12"

    @override
    def get_version_command(self) -> str | None:
        return f"{PY} -m karox6 --version"

    @override
    async def install(self, environment: BaseEnvironment) -> None:
        if not self._wheel_path or not self._wheel_path.is_file():
            raise RuntimeError(f"karox6 wheel not found: {self._wheel_path}")
        await self.ensure_system_dependencies(environment, ("python3",))
        target = "/tmp/" + self._wheel_path.name  # pip checks the basename against metadata
        await environment.upload_file(str(self._wheel_path), target)
        if environment.default_user is not None:
            await self.exec_as_root(
                environment,
                command=f"chown {shlex.quote(str(environment.default_user))} {shlex.quote(target)}",
            )
        script = INSTALL.replace("{venv}", VENV).replace("{py}", PY)
        await self.exec_as_agent(
            environment, command=script.replace("{wheel}", shlex.quote(target))
        )

    def build_command(self, instruction: str) -> str:
        options: KaroX6Options = self.options  # type: ignore[assignment]
        task_dir = shlex.quote(options.task_dir or "/app")
        flags = [
            "--json",
            "--provider", "openai-chat",
            "--base-url", GATEWAY_BASE,
            "--api-key-env", KEY_ENV,
            "--model", shlex.quote(options.model_alias),
            "--context-window", str(int(options.context_window)),
            "--max-output-tokens", str(int(options.max_output_tokens)),
            "--home", HOME,
            "--cwd", task_dir,
            "--approve-dangerous", "deny",
        ]
        if options.max_seconds is not None:
            flags += ["--max-seconds", str(int(options.max_seconds))]
        if options.max_steps is not None:
            flags += ["--max-steps", str(int(options.max_steps))]
        if options.extra_flags:
            flags += [shlex.quote(word) for word in shlex.split(options.extra_flags)]
        return (
            f"mkdir -p {HOME} && cd {task_dir} && "
            f"{PY} -m karox6 run {' '.join(flags)} -- {shlex.quote(instruction)} "
            f"</dev/null 2>{STDERR} | stdbuf -oL tee {EVENTS}"
        )

    @override
    async def run(
        self, instruction: str, environment: BaseEnvironment, context: AgentContext
    ) -> None:
        key = (getattr(self, "_extra_env", None) or {}).get(KEY_ENV, "")
        if not key:
            raise ValueError(f"{KEY_ENV} missing: pass it via agents[].env")
        await self.exec_as_agent(
            environment, env={KEY_ENV: key}, command=self.build_command(instruction)
        )

    @override
    def populate_context_post_run(self, context: AgentContext) -> None:
        """Token usage from the run_finished event (KaroX's own count; the gateway audit
        stays the source of truth for the report)."""
        path = self.logs_dir / "karox6.jsonl"
        if not path.exists():
            return
        usage = None
        for line in path.read_text(errors="replace").splitlines():
            try:
                event = json.loads(line)
            except ValueError:
                continue
            if isinstance(event, dict) and event.get("type") == "run_finished":
                usage = event.get("usage") or {}
        if usage:
            context.n_input_tokens = int(usage.get("input_tokens") or 0)
            context.n_cache_tokens = int(usage.get("cached_tokens") or 0)
            context.n_output_tokens = int(usage.get("output_tokens") or 0)


class KaroX6B(KaroX6):
    """The same agent as a second arm (A/B variant flags or wheel) in the same job."""

    @staticmethod
    @override
    def name() -> str:
        return "karox6b-hard12"
