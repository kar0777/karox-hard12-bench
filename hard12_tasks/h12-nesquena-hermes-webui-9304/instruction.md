You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

POST /api/default-model persists the picker's provider routing id into model.provider, breaking every later turn

## Summary

`set_hermes_default_model()` persists the request's `provider` verbatim:

```python
# api/config.py:7654
persisted_provider = str(requested_provider or resolved_provider or previous_provider or "").strip()
```

When a model is picked from a **non-default provider group**, the Settings picker sends a
**provider + model pin** in that field — e.g. `nous:meituan/longcat-2.5`. That is the same
form `/api/models` reports as `active_provider` and uses for its group ids; it is **not** a
provider the agent registers. Writing it to `config.yaml -> model.provider` poisons the
config for every consumer.

## Reproduction

```bash
# 1. Save a model the way the Settings UI does
curl -s -X POST http://127.0.0.1:8787/api/default-model \
  -H 'Content-Type: application/json' \
  -d '{"model": "meituan/longcat-2.5:free", "provider": "nous:meituan/longcat-2.5"}'
# -> {"ok": true, "model": "meituan/longcat-2.5:free", "provider": "nous:meituan/longcat-2.5"}

# 2. config.yaml now contains:
#    model:
#      default: meituan/longcat-2.5:free
#      provider: nous:meituan/longcat-2.5

# 3. Every subsequent turn fails
```

Reachability: `POST /api/default-model` (`api/routes.py:20822`) and
`POST /api/model/set` with `scope: "main"` (`api/routes.py:20844`) both feed the request's
`provider` straight into `set_hermes_default_model()`.

## Observed failures

| Surface | Error |
|---|---|
| CLI | `Unknown provider 'nous:meituan/longcat-2.5'. Check 'hermes model' for available providers, or run 'hermes doctor'` |
| WebUI | `[webui] WARNING: resolve_runtime_provider failed: Unknown provider 'nous:meituan/longcat-2.5'` followed by `[webui] stream error:` |

Note the WebUI keeps serving and `/api/health/agent` still looks fine, so this presents as
"chats suddenly stopped working after I changed the model", not as a config error.

## Impact

One click in the model picker silently breaks chatting on both the WebUI and the CLI until
the user hand-edits `config.yaml`. Recovery is not discoverable from the UI.

## Suggested fix

Validate the requested provider before persisting it. If it is not a provider the agent can
actually use, discard it and let the existing
`requested_provider or resolved_provider or previous_provider` chain fall through to the
provider the model itself resolves to.

The picker's `provider` field is a WebUI routing id, not an agent provider id: for a
non-default group it carries a model pin (`nous:meituan/longcat-2.5`), which is the same form
`/api/models` reports as `active_provider`. The agent has no such provider registered, so the
value must never reach `config.yaml`. A real provider id (`nous`, `gemini`, `custom:…`) is
unaffected and should keep being persisted exactly as today.

`_is_known_model_provider()` (`api/config.py:1642`) already provides this classification for
the static tables and `custom:`-style ids. It needs one companion check for providers declared
under `providers:` in `config.yaml` — e.g. a named `ollama-launch` — because those are not in
the static tables and would otherwise be wrongly discarded.

```python
def _provider_is_persistable(provider_id, config_data=None) -> bool:
    pid = str(provider_id or "").strip().lower()
    if not pid:
        return False
    if _is_known_model_provider(pid):
        return True
    providers = (config_data or {}).get("providers")
    return isinstance(providers, dict) and pid in {str(k).strip().lower() for k in providers}
```

and in `set_hermes_default_model()`, immediately after `requested_provider` is read:

```python
if requested_provider and not _provider_is_persistable(requested_provider, config_data):
    logger.warning(
        "ignoring unknown default-model provider %r; using the model's resolved provider",
        requested_provider,
    )
    requested_provider = ""
```

Placing the guard before `resolve_model_provider()` keeps `resolved_provider` authoritative
for a discarded pick, and leaves `provider_override_won` (which compares `requested_provider`
against `resolved_provider`) correct. `config_data` is already loaded in that block, so the
`providers:` check is free.

### Behaviour after the fix

| Request | `model.provider` written |
|---|---|
| `provider: "nous:meituan/longcat-2.5"` (picker pin) | `nous` — pin discarded, model's own resolution used |
| `provider: "gemini"` (real provider) | `gemini` — persisted unchanged |
| `provider: "ollama-launch"` (config-declared) | `ollama-launch` — persisted unchanged |
| no `provider` | unchanged (existing fallback) |

Verified against a live WebUI: the bad form now returns `provider: "nous"` and leaves
`config.yaml` untouched, a legitimate pick still persists, and a subsequent chat turn
succeeds.

Reproduced on `676d4f9b2` (2026-11-21) and on a July 2026 checkout; the offending line is
unchanged in both.

## Related (adjacent, not duplicates)

- #7260 — auxiliary model settings persist `@provider:model` routing ids as model names
- #6131 — Settings model switch does not persist `model.provider` for cross-provider ids
- #895 — saving an `@nous:` default model strips the prefix
- #7346 — slash-id picks from a non-active custom-provider group lose the provider hint

