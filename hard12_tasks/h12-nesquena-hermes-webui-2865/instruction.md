You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

bug(session): new_session() stamps display.personality onto every session at creation (regression from #2747)

# `new_session()` stamps `display.personality` onto every session at creation (regression from #2747)

## Summary

[PR #2747](https://github.com/nesquena/hermes-webui/pull/2747) (commit `4153a47d`, merged via stage-403 on May 22 2026) made `new_session()` read `display.personality` from `config.yaml` and pass it as the default `personality=` kwarg to `Session(...)`. Because `Session.personality` is a persistent field that survives reloads and gets serialised through `state.db`, this turns a `display.*` config key into stamped-at-creation per-session state.

That's a layering inversion: `display.*` is the cosmetic config block, but one of its values now has memory. The original goal — "make `/personality taleb` sticky for new sessions" — was reasonable, but the implementation took it further than it needed to.

Reported by @AvidFuturist (Discord, May 24 2026), who hit the worst version of this downstream where fork-specific profile-scoped response modes are silently overridden by a stale global `display.personality` value.

## Repro

1. In `~/.hermes/config.yaml`:
   ```yaml
   display:
     personality: kawaii
   agent:
     personalities:
       kawaii:
         system_prompt: "Respond very cutely."
       taleb:
         system_prompt: "Channel Nassim Taleb."
   ```
2. Restart WebUI.
3. Create a new session and inspect its serialised form.

**Expected:** `session.personality` is `None` until the user runs `/personality <name>` explicitly. `display.*` config should not stamp persistent state.

**Actual:** Every newly created session has `personality="kawaii"` baked in (api/models.py line 1968). Changing `display.personality` in `config.yaml` later does not roll forward to existing sessions — the stamped value wins. Every existing session continues to carry the old value forever.

## Root cause

`api/models.py` lines 1948-1968 (introduced in 4153a47d):

```python
# Read default personality from config display.personality
_default_personality = None
try:
    from api.config import get_config as _get_cfg_for_personality
    _cfg_personality = (_get_cfg_for_personality().get('display') or {}).get('personality')
    if _cfg_personality and isinstance(_cfg_personality, str):
        _cfg_personality = _cfg_personality.strip().lower()
        if _cfg_personality and _cfg_personality not in ('default', 'none', 'neutral'):
            _default_personality = _cfg_personality
except Exception:
    pass

...
s = Session(
    ...,
    personality=_default_personality,
    ...,
)
```

`Session.__init__` (line 401) stores it as `self.personality`, line 709 serialises it into the session dict, `Session.save()` persists to `state.db`. The intent was "default fallback"; the effect is "permanent stamp."

`api/streaming.py:4242-4261` then reads `getattr(s, 'personality', None)` (the stamped value) at every chat turn to build `ephemeral_system_prompt`. The config is **never re-consulted** at stream time.

## Problems

1. **Layering violation.** `display.*` should not own persistent session state. Tests in `tests/test_default_personality.py` (R1: `display.personality='taleb'` → `s.personality=='taleb'`) lock this contract in.
2. **Staleness.** Changing `display.personality` later in `config.yaml` doesn't roll forward to existing sessions — every old session keeps the value it was stamped with, and the user can't tell which.
3. **Override surprise for downstream / profile work.** Any runtime overlay system (profile-scoped personalities, SOUL response modes downstream, future `/personality` semantics) has to fight a stamped value instead of stacking on top of `None`.

## Proposed fix

Resolve `display.personality` as a **render-time fallback** in `api/streaming.py`, not as a stamped session attribute. Drop the `new_session()` config read.

```python
# api/streaming.py ~line 4242
_pname = getattr(s, 'personality', None)
if not _pname:
    _pname = (_cfg.get('display') or {}).get('personality')
    if _pname and isinstance(_pname, str):
        _pname = _pname.strip().lower()
        if _pname in ('', 'default', 'none', 'neutral'):
            _pname = None
```

Effect:

- The "sticky default" UX is preserved: `display.personality: taleb` still applies to every new session that hasn't been explicitly overridden.
- `display.personality` becomes a live fallback — change it in `config.yaml` and existing sessions follow.
- `/personality <name>` still pins per-session as before (sets `s.personality` directly).
- Downstream profile-scoped overlays can win cleanly when `s.personality is None`.

Tests in `tests/test_default_personality.py` need rewriting against the new contract (assert ephemeral prompt content, not `s.personality` value).

## Why this slipped through

- PR #2747 looked like a small UX nicety; the persistence side-effect wasn't called out in review.
- The merged-in tests pinned the *wrong* contract (R1 asserts `s.personality == "taleb"`), making the layering bug look like the spec rather than the bug.
- No existing test covered "change `display.personality` and verify existing sessions update" — the staleness path is invisible.

## User-facing impact

- Upstream: `display.personality` silently becomes write-once-stamped. Users editing `config.yaml` see no effect on existing sessions and have no path back to "neutral" short of `/personality default` on each session.
- Downstream / forks: profile-scoped personality systems get clobbered by a stale global default.

## Files involved

- `api/models.py` lines 1948-1968 — remove the config read + the `personality=_default_personality` kwarg
- `api/streaming.py` near line 4242 — add the render-time `display.personality` fallback
- `tests/test_default_personality.py` — rewrite to assert ephemeral prompt behaviour, not stamped session attribute

## Credit

Reported by @AvidFuturist with fork experience showing the broader impact pattern. Original PR by @s010mn.

## Suggested labels

`bug`, `regression`, `sprint-candidate`

