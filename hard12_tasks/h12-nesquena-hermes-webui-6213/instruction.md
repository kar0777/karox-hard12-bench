You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

tech(contract): expose msg_limit ceiling in /api/session metadata so the frontend doesn't hand-mirror _MAX_MSG_LIMIT

## Context

PR #6152 introduced a server-side ceiling on `GET /api/session ?msg_limit=` (`_MAX_MSG_LIMIT = 500`, `api/routes.py`). PR #6154 fixed the two frontend paths that relied on unbounded `msg_limit` (outline jump, endless scroll) and added a hand-mirrored `_MSG_LIMIT_MAX = 500` constant in `static/sessions.js` so the frontend knows when to switch from the growing-tail strategy to `msg_before` paging.

Both #6152 and #6154 reviewers (Greptile and maintainer) flagged the same fragility: **the two constants are coupled by hand with no automated guard.** If the backend ceiling changes and the frontend mirror isn't updated, load-older silently stalls again at the old value — the exact regression #6154 fixed — with no test to catch it.

## Proposal

Surface the ceiling in the `/api/session` response metadata (alongside the existing `_messages_offset` / `_messages_truncated` fields), e.g. a `_msg_limit_max` field, and have the frontend read it instead of hardcoding `_MSG_LIMIT_MAX`.

Rough shape:
- Backend (`api/routes.py`): add `raw["_msg_limit_max"] = _MAX_MSG_LIMIT` to the `GET /api/session` response (near where `_messages_truncated` is set, ~line 12708).
- Frontend (`static/sessions.js`): read `data.session._msg_limit_max` on load (default to the current `500` literal if absent for backward-compat with older servers), and use it as the threshold in `_loadOlderMessages`'s `useBeforePaging` check.
- Drop the hand-mirrored `_MSG_LIMIT_MAX` constant (or keep it only as the fallback default).

This removes the coupling entirely — the frontend always follows whatever the server's actual ceiling is.

## Why track separately

This spans both #6152 (backend) and #6154 (frontend) and changes a response contract field, so it shouldn't be silently folded into either. It's also strictly a hardening follow-up — #6154's mirror works correctly today; this just removes the maintenance footgun.

## Optional automated guard (until the metadata exposure lands)

Until the metadata field ships, a static-source assertion test could read both `api/routes.py` (`_MAX_MSG_LIMIT = <N>`) and `static/sessions.js` (`_MSG_LIMIT_MAX = <N>`) and fail if they differ. The repo already has a JS-source-reading test helper (`tests/js_source_extract.py`), so this is cheap. This is a stopgap; the metadata exposure above is the real fix.

## References

- #6152 — backend `msg_limit` ceiling
- #6154 — frontend follow-up (introduces the `_MSG_LIMIT_MAX` mirror this issue would retire)
- Maintainer comment on #6154 flagging the coupling

## Model Used

builtin:zai-coding-plan/GLM-5.2 (ZCode agent).

