You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

bug(cron): active cron sessions wrongly appear as completed in sidebar

**Bug:** an active (still-running) cron job's session is painted as *completed* in the sidebar the moment it appends a new message, before the job actually finishes.

### Repro
1. Trigger a cron job that runs for a while (scheduled or via `/api/crons/run`).
2. Watch its session row in the sidebar while the job is mid-run.
3. As soon as a new message lands, the row picks up a completion/unread dot.

**Expected:** the row shows an active/running indicator while the job executes and flips to completed only when the job ends.

## Root cause (split-brain between two server state sources the sidebar never reconciles)
- Cron liveness lives only in the in-memory `_RUNNING_CRON_JOBS` dict — `api/routes.py:1328-1344` (`_mark_cron_running` / `_mark_cron_done` / `_is_cron_running`) — and is surfaced **only** via `/api/crons/status` (`_handle_cron_status`, `api/routes.py:20345`).
- The sidebar polls **only** `/api/sessions`, deriving "running" from session-row fields via `_isSessionEffectivelyStreaming` (`static/sessions.js:814`). Cron rows never get `is_streaming=True`, so the completion heuristic in `_markPollingCompletionUnreadTransitions` (`static/sessions.js:1188`) trips `completedWithNewMessages` (line 1217) on every mid-run message.
- The existing cron guard (lines 1236-1247) filters only by **profile**, never by whether the job is still running.

## Suggested fix
- **Server:** in `_build_session_list_cache_payload` (`api/routes.py:2159`), mark cron rows whose `session_id` matches `_is_cron_running` with `is_streaming`/`cron_running`.
- **Client:** `_markPollingCompletionUnreadTransitions` should skip/defer "completed" for cron-source rows while the job runs (honor the flag or gate on real job completion).

## Related
- `tests/test_issue4385_cron_archive_reappears.py` (cron row identity contract — must not stamp cron as CLI).
- Present on `upstream/master` `320789ae` (2026-07-31); verified code path, not yet live-repro'd.
