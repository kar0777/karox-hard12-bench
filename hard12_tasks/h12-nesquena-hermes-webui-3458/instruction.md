You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Gateway health remote probe: fix probe order (/health/detailed) + unify on GATEWAY_HEALTH_URL (follow-up to #3312)

## Summary

Two related follow-ups to #3312 (v0.51.200), which added a remote-gateway health probe via `HERMES_API_URL` so multi-container Docker deployments stop showing a spurious "Gateway not configured" banner. The fix is correct and strictly better than the prior baseline, but two refinements surfaced in pre-release review that would make the remote probe actually populate health details and stop diverging from the rest of the codebase's gateway-URL convention.

## 1. Probe order misses the endpoint that carries `gateway_state`

**Current behavior** (`api/agent_health.py`, the remote-probe path added in #3312): probes `/status` (and `/api/gateway/status`) first.

**Problem:** `gateway/platforms/api_server.py` only registers `/health`, `/health/detailed`, and `/v1/health`. `/status` and `/api/gateway/status` never match a handler. `/health` returns a static `{"status":"ok"}` with no detail; **`/health/detailed` is the only endpoint that carries `gateway_state`**, which is what `api/routes.py` (~5338-5342) reads to populate the stale-running detail case.

**Proposed fix:** probe `/health/detailed` first (or include it in the probe set ahead of `/status`), so the remote-probe payload can populate `details["gateway_state"]` for the running/stale-running case rather than only resolving the binary alive/not-configured state.

## 2. Env-var split-brain: `HERMES_API_URL` vs the repo's `GATEWAY_HEALTH_URL` convention

**Current behavior:** #3312 reads a new env var `HERMES_API_URL`.

**Problem:** the rest of the repo standardizes on `GATEWAY_HEALTH_URL` / `HERMES_GATEWAY_HEALTH_URL` (see `api/updates.py` ~269-280, default `http://hermes-agent:8642`) via the `_gateway_health_base_url()` helper. Introducing a third, otherwise-unreferenced name means a deployment can have one cross-container probe working while the other silently no-ops, and the bug reporter's original compose set `HERMES_API_URL` on the *workspace* container, not the webui container — so even the new var won't fire for that setup without doc changes.

**Proposed fix:** have the new probe reuse `_gateway_health_base_url()` (with its `http://hermes-agent:8642` default) instead of reading `HERMES_API_URL` directly — or, if `HERMES_API_URL` must be supported for compatibility, treat it as an alias resolved inside that one helper so there is a single source of truth for the gateway base URL. Update `docs/docker.md` to name whichever var(s) the webui container reads.

## Scope

**In scope:** probe-order change in the `api/agent_health.py` remote path; unifying the gateway-base-URL resolution onto `_gateway_health_base_url()`; a doc note in `docs/docker.md` naming the env var(s) the webui container reads for gateway health.

**Out of scope:** the baseline #3312 behavior (already shipped and correct); any change to the gateway's own registered endpoints; single-container deployments (unaffected — they keep the local `gateway.status` import path when no remote URL is set).

## Verification

- Multi-container Docker: with the gateway up and the correct env var set on the webui container, the Tasks/Cron panel shows a healthy gateway with populated `gateway_state` (not just non-amber).
- With the gateway down: panel reports gateway-down (`running:false`), not a false-green.
- Single-container: unchanged — local probe still used when no remote URL configured.
- A regression test driving the remote-probe path with a fake `/health/detailed` payload asserting `gateway_state` populates.

Surfaced in the v0.51.200 pre-release Opus review of #3312. Filing rather than holding the release because the shipped behavior is strictly no worse than the pre-PR baseline.

