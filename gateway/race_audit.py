"""LiteLLM proxy callback for the four-harness race.

1. Enforces the frozen inference profile (config/inference_profile.json) on the
   FINAL provider kwargs, whatever client protocol the harness spoke.
2. Refuses any request whose alias is not one of the four race aliases.
3. Appends one sanitized JSON line per provider attempt to
   $HARNESS_RACE_AUDIT_DIR/audit.jsonl. No message content, no secrets.

Run attribution: the controller writes $HARNESS_RACE_AUDIT_DIR/context/<harness>.json
({"run_id":..., "task_id":...}) before a run; the alias identifies the harness.
"""
from __future__ import annotations

import json
import os
import threading
import time
from pathlib import Path
from typing import Any, Optional

try:  # pragma: no cover - imported inside the gateway only
    from litellm.integrations.custom_logger import CustomLogger
except Exception:  # noqa: BLE001 - unit tests import without litellm
    class CustomLogger:  # type: ignore[no-redef]
        pass

HERE = Path(__file__).resolve().parent
# HARNESS_RACE_PROFILE lets a separate gateway instance (e.g. HARD12) use its
# own frozen profile; unset keeps the race default.
PROFILE = json.loads(Path(
    os.environ.get("HARNESS_RACE_PROFILE") or (HERE.parent / "config" / "inference_profile.json")
).read_text(encoding="utf-8"))
ALIASES: dict[str, str] = PROFILE["aliases"]
ENFORCED: dict[str, Any] = PROFILE["enforced"]
STRIPPED = tuple(PROFILE["stripped_request_fields"])
UPSTREAM_MODEL = PROFILE["upstream_model"]
_LOCK = threading.Lock()


def audit_dir() -> Path:
    return Path(os.environ.get("HARNESS_RACE_AUDIT_DIR") or (HERE.parent / "logs" / "gateway"))


def _context(harness: str) -> dict:
    path = audit_dir() / "context" / f"{harness}.json"
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def enforce_profile(kwargs: dict) -> dict:
    """Normalize provider kwargs (OpenAI chat shape) to the frozen profile."""
    for field in STRIPPED:
        kwargs.pop(field, None)
    for key, value in ENFORCED.items():
        kwargs[key] = value
    if "reasoning_effort" in ENFORCED:  # stepfun-style upstreams only
        allowed = list(kwargs.get("allowed_openai_params") or [])
        if "reasoning_effort" not in allowed:
            allowed.append("reasoning_effort")
        kwargs["allowed_openai_params"] = allowed
    extra = kwargs.get("extra_body")
    if isinstance(extra, dict):
        for field in STRIPPED:
            extra.pop(field, None)
    return kwargs


def sanitize_sent(kwargs: dict) -> dict:
    """The non-content parameters of a request, for the audit line."""
    keep = ("model", "temperature", "top_p", "reasoning_effort", "max_tokens", "stream",
            "tool_choice", "parallel_tool_calls", "stop")
    out = {k: kwargs[k] for k in keep if k in kwargs}
    tools = kwargs.get("tools")
    if isinstance(tools, list):
        out["tools_count"] = len(tools)
    msgs = kwargs.get("messages")
    if isinstance(msgs, list):
        out["messages_count"] = len(msgs)
        out["tool_result_messages"] = sum(1 for m in msgs if isinstance(m, dict) and m.get("role") == "tool")
    stripped_present = [k for k in STRIPPED if k in kwargs]
    if stripped_present:
        out["stripped_fields_still_present"] = stripped_present
    return out


def write_record(record: dict) -> None:
    path = audit_dir() / "audit.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(record, ensure_ascii=False, default=str)
    with _LOCK, path.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def _usage(obj: Any) -> dict:
    usage = getattr(obj, "usage", None)
    if usage is None and isinstance(obj, dict):
        usage = obj.get("usage")
    if usage is None:
        return {}
    if hasattr(usage, "model_dump"):
        usage = usage.model_dump()
    if not isinstance(usage, dict):
        return {}
    ptd = usage.get("prompt_tokens_details") or usage.get("input_tokens_details") or {}
    ctd = usage.get("completion_tokens_details") or usage.get("output_tokens_details") or {}
    prompt = usage.get("prompt_tokens")
    completion = usage.get("completion_tokens")
    cached = ptd.get("cached_tokens") if isinstance(ptd, dict) else None
    if prompt is None and usage.get("input_tokens") is not None:
        if "cache_read_input_tokens" in usage or "cache_creation_input_tokens" in usage:
            # Anthropic shape: input_tokens EXCLUDES cache reads/creations.
            cache_read = int(usage.get("cache_read_input_tokens") or 0)
            prompt = int(usage["input_tokens"]) + cache_read + int(usage.get("cache_creation_input_tokens") or 0)
            cached = cache_read
        else:  # Responses shape: input_tokens already includes cached tokens.
            prompt = usage["input_tokens"]
    if completion is None:
        completion = usage.get("output_tokens")
    return {
        "input_tokens": prompt,
        "cached_input_tokens": cached,
        "output_tokens": completion,
        "reasoning_tokens": ctd.get("reasoning_tokens") if isinstance(ctd, dict) else None,
        "total_tokens": usage.get("total_tokens"),
    }


def _reported_model(obj: Any) -> Optional[str]:
    if obj is None:
        return None
    if isinstance(obj, dict):
        return obj.get("model")
    return getattr(obj, "model", None)


def _alias_of(kwargs: dict) -> Optional[str]:
    meta = (kwargs.get("litellm_params") or {}).get("metadata") or kwargs.get("metadata") or {}
    slo = kwargs.get("standard_logging_object") or {}
    alias = slo.get("model_group") or meta.get("model_group") or kwargs.get("model_group")
    if not alias and kwargs.get("model") in ALIASES:  # failures raised before routing keep the public alias
        alias = kwargs.get("model")
    return alias


class RaceAudit(CustomLogger):
    """Profile enforcement + audit trail."""

    async def async_pre_call_hook(self, user_api_key_dict, cache, data: dict, call_type):  # noqa: ANN001
        alias = data.get("model")
        if alias not in ALIASES:
            raise ValueError(f"harness-race gateway serves only the race aliases, not {alias!r}")
        meta = data.setdefault("metadata", {})
        if isinstance(meta, dict):
            requested = {k: data.get(k) for k in ("temperature", "top_p", "max_tokens", "max_output_tokens",
                                                   "reasoning_effort", "reasoning", "thinking") if k in data}
            meta["race_requested_params"] = json.dumps(requested, default=str)[:400]
            meta["race_call_type"] = str(call_type)
        return data

    async def async_pre_call_deployment_hook(self, kwargs: dict, call_type):  # noqa: ANN001
        return enforce_profile(kwargs)

    def _record(self, kwargs: dict, response_obj: Any, start_time: Any, end_time: Any, status: str) -> None:
        slo = kwargs.get("standard_logging_object") or {}
        alias = _alias_of(kwargs)
        harness = ALIASES.get(alias or "", "unknown")
        ctx = _context(harness)
        meta = (kwargs.get("litellm_params") or {}).get("metadata") or {}
        sent = (kwargs.get("additional_args") or {}).get("complete_input_dict")
        try:
            latency = (end_time - start_time).total_seconds()
        except Exception:  # noqa: BLE001
            latency = None
        record = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "harness": harness,
            "run_id": ctx.get("run_id"),
            "task_id": ctx.get("task_id"),
            "requested_alias": alias,
            "upstream_model_config": kwargs.get("model"),
            "upstream_model_reported": _reported_model(response_obj),
            "api_base": slo.get("api_base") or (kwargs.get("litellm_params") or {}).get("api_base"),
            "call_type": meta.get("race_call_type") or kwargs.get("call_type"),
            "client_requested": meta.get("race_requested_params"),
            "sent": sanitize_sent(sent if isinstance(sent, dict) else {k: kwargs.get(k) for k in (
                "model", "temperature", "top_p", "reasoning_effort", "max_tokens", "stream") if k in kwargs}),
            "sent_source": "complete_input_dict" if isinstance(sent, dict) else "kwargs",
            "latency_s": latency,
            "stream": bool(kwargs.get("stream")),
            "status": status,
            "retry_attempt": (kwargs.get("litellm_params") or {}).get("metadata", {}).get("attempted_retries"),
        }
        record.update(_usage(response_obj))
        if status != "success":
            exc = kwargs.get("exception")
            record["error"] = f"{type(exc).__name__}: {str(exc)[:300]}" if exc else str(slo.get("error_str"))[:300]
        write_record(record)

    async def async_post_call_failure_hook(self, request_data, original_exception, user_api_key_dict,
                                           traceback_str=None):  # noqa: ANN001
        """Proxy-level failures (e.g. protocol-bridge 400s) that never reach the provider logger."""
        alias = request_data.get("model") if isinstance(request_data, dict) else None
        harness = ALIASES.get(alias or "", "unknown")
        ctx = _context(harness)
        write_record({
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "event": "proxy_failure",
            "harness": harness,
            "run_id": ctx.get("run_id"),
            "task_id": ctx.get("task_id"),
            "requested_alias": alias,
            "status": "failure",
            "error": f"{type(original_exception).__name__}: {str(original_exception)[:300]}",
        })

    async def async_log_success_event(self, kwargs, response_obj, start_time, end_time):  # noqa: ANN001
        self._record(kwargs, response_obj, start_time, end_time, "success")

    async def async_log_failure_event(self, kwargs, response_obj, start_time, end_time):  # noqa: ANN001
        self._record(kwargs, response_obj, start_time, end_time, "failure")


proxy_handler_instance = RaceAudit()
