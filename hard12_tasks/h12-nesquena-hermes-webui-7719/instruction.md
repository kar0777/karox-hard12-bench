You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Archive on a cross-profile session fails with misleading "Session not found" (404) instead of 409

## Environment

- hermes-webui browser dashboard served on `http://127.0.0.1:8787`
- Multi-profile setup (at least two profiles), sidebar showing sessions from all profiles
- Local checkout: `adbb3258` (2026-09-17), tag `exp-v0.52.318`, branch master behind origin/master by 101 commits

## Summary

With sessions from other profiles visible in the sidebar, archiving such a session fails with a toast:

> Archive failed: Session not found

The session exists and opens fine (clicking it auto-switches the active profile and loads it). The failure comes from the request-level profile-visibility guard, which reports a profile mismatch as a missing session — the same mismatch that the session detail endpoint reports correctly with HTTP 409.

## Steps to reproduce

1. Have at least two profiles, each with at least one WebUI session.
2. Enable showing sessions from other profiles in the sidebar.
3. Open the context menu of a session that belongs to a non-active profile → **Archive conversation**.

**Actual:** `Archive failed: Session not found`.
**Expected:** the action succeeds (the session is visible and owned by the user), or the server returns a profile-mismatch signal so the client can react meaningfully.

## Wire evidence (captured from the running instance)

```
POST /api/session/archive  {"session_id":"<id>","archived":true}
-> 404 {"error": "Session not found"}

GET /api/session?session_id=<same id>
-> 409 {"error": "Session belongs to a different profile",
        "code": "session_profile_mismatch", "session_id": "<id>", "profile": "def"}
```

Same session id, same moment: the detail endpoint reports a profile mismatch, archive masks it as 404.

## Root cause

`POST /api/session/archive` goes through the generic request guard `_guard_request_session_visibility(...)` (`api/routes.py`, `method="POST"` branch). Inside, `_session_id_visible_to_request_profile()` resolves the session, compares its stored `profile` against the active request profile, and on mismatch calls `bad(handler, "Session not found", 404)` — for a session that was in fact found, just owned by another profile.

Compare with the detail endpoint `GET /api/session`, which handles the identical situation properly (`api/routes.py` ~13028):

```python
if not _session_visible_to_active_profile(_session_profile, handler):
    if _session_profile:
        # Valid session owned by a KNOWN other profile: 409 so the
        # client can offer to switch to it (#5419).
        return j(handler, {
            "error": "Session belongs to a different profile",
            "code": "session_profile_mismatch",
            "session_id": sid,
            "profile": _session_profile,
        }, status=409)
```

Archive has no such branch, so the mismatch is masked as "not found" — which reads like data loss to the user.

## Affected scope

Any mutation that passes `session_id` in a POST/PATCH/DELETE body and is covered by `_guard_request_session_visibility` (e.g. rename, move, pin, delete) presumably behaves the same way. Only archive was verified end-to-end.

## Suggested fix

1. In `_session_id_visible_to_request_profile()` (and/or the guard), distinguish "profile mismatch" from "session missing": return `409` with `code: session_profile_mismatch` and the owning profile for mutations, mirroring the detail-load behavior.
2. Frontend: on `409 session_profile_mismatch` either auto-switch profile before performing the action (consistent with what clicking a cross-profile session in the sidebar already does), or show an actionable error instead of "Session not found".

Auto-switching on click but failing with "not found" on archive is inconsistent UX for the same object in the same list.

---
*Note: this was initially filed against NousResearch/hermes-agent ([#118242](https://github.com/NousResearch/hermes-agent/issues/118242)) by mistake and closed after the correct repo was identified.*
