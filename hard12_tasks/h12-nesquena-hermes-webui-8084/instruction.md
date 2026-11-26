You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Self-locked truncation_watermark silently drops all post-compression turns

## Summary

A session can enter a permanently frozen transcript after compression. New turns keep arriving in `state.db`, but the WebUI keeps rendering an old snapshot — with no error surfaced anywhere. On one real session this silently dropped several thousand messages (including every subsequent user turn) while the session itself kept running.

The freeze is a **self-lock**: the rows that would advance the sidecar past the watermark are exactly the rows the watermark hides.

## Root cause

`_advance_truncation_watermark_after_commit` (`api/streaming.py`) falls back to `time.time()` when the committed turn carries no timestamped user row — the shape produced by a gateway handoff or a background-process notification turn:

```python
for msg in reversed(messages):
    if msg.get('role') == 'user':
        ts = msg.get('timestamp')
        if isinstance(ts, (int, float)) and ts > 0:
            session.truncation_watermark = float(ts)
            return
session.truncation_watermark = time.time()   # <-- wall clock
```

That wall-clock value is **newer than every row in the sidecar**. The append-only merge's `sidecar_advanced_past_watermark` guard is the only path that lets newer `state.db` rows merge back, and it requires the sidecar's own max timestamp to exceed the watermark — so it stays `False` forever:

```
max_sidecar_timestamp < watermark   ->  False
watermark_advanced_by_boundary      ->  False
=> sidecar_advanced_past_watermark  ->  False
```

Every `state.db` row above the watermark is then dropped as a "replaced tail", and every unseen row below it is dropped as a "stale replaced row". The session cannot recover: I verified empirically that the next turn does **not** restore it.

The broken invariant: **a legitimate watermark always equals a real message timestamp** — `session_ops._truncation_watermark_for` uses the last kept row's timestamp. A value newer than every row can never be a real truncate cutoff.

### Observed impact (one long-running compressed session)

Times are relative to the freeze, not absolute.

| Measurement | Value |
|---|---|
| Sidecar newest message | ~3h25m before the watermark |
| Watermark | wall clock; **no `state.db` row exists at that second** |
| Rows dropped above the watermark | ~1.6k |
| Rows dropped below the watermark | ~1.8k |
| Sidecar size vs `state.db` | 275 vs ~3.5k |
| Session still running? | Yes — still receiving rows hours later |

## Reproduction shape

```python
# Sidecar frozen at 100; watermark is a wall-clock value past every sidecar row.
sidecar = [{"role": "user", "content": "q1", "timestamp": 50},
           {"role": "assistant", "content": "a1", "timestamp": 100}]
state   = sidecar + [{"role": "user", "content": "q2", "timestamp": 200},
                     {"role": "assistant", "content": "a2", "timestamp": 250}]

merged = merge_session_messages_append_only(
    sidecar, state, truncation_watermark=9999.0, truncation_boundary=9999.0)
# merged == sidecar  -> q2/a2 silently dropped forever
```

## Proposed fix

1. **`api/streaming.py`** — clamp to the newest *real* message timestamp instead of inventing a wall-clock boundary; keep the existing value when no row carries a timestamp (a too-old watermark only over-filters, it cannot self-lock).
2. **`api/routes.py`** — `_checkpoint_user_message_for_eager_session_save` inlines the same fallback; apply the same invariant.
3. **`api/models.py`** — the merge detects a stale wall-clock watermark (newer than every sidecar row, impossible for a legitimate cutoff) and ignores it, **failing OPEN toward data** rather than silently dropping turns. This also recovers sessions already frozen by this bug, without a manual sidecar edit.

## Invariants preserved

Verified unchanged:

- `#2914` `0.0` truncate-to-empty sentinel still blocks all replay
- Legitimate edit/retry/undo watermarks still suppress the replaced tail
- Same-second replaced-user guard still applies
- `#3831` advanced-watermark filtering of pre-edit rows

## State layer mutated

`truncation_watermark` / `truncation_boundary` on the WebUI session sidecar, and the `sidecar_advanced_past_watermark` decision inside the append-only `state.db` merge. `state.db` itself is read-only in this path and remains the durable source of truth.

## Verification

- New `tests/test_stale_watermark_self_heal.py` (13 cases). 5 of them fail against the unpatched product code and pass with the fix.
- `test_issue3831_watermark_clear.py::test_advance_helper_uses_current_time_when_no_timestamp` asserted the buggy wall-clock behavior; replaced with `test_advance_helper_never_stamps_wall_clock_when_no_timestamp`.
- Targeted + neighbouring suites: **100 passed**.
- Full-suite A/B against a pristine `HEAD` export using an identical command: 462 unique failures on both sides, **set difference 0**.
- Live session through the browser's own display path: **279 → ~1.8k visible messages**, newest advancing from hours-old to the live edge.

The full-suite `FileNotFoundError` cascade in the numbers above is a pre-existing local test-harness issue (the isolated test server cannot write its log under the sandbox temp root). It reproduces on pristine `HEAD` and is unrelated to this change.

## Contract Routing

- **Task type:** bug fix (data loss), runtime/session-recovery path
- **Touched areas:** session metadata (`truncation_watermark`), append-only `state.db` merge, compression recovery
- **Relevant public docs:** `AGENTS.md` (runtime/recovery/compression invariants), `docs/CONTRACTS.md`, `docs/rfcs/webui-run-state-consistency-contract.md`
- **Scope boundaries:** no changes to `state.db` schema or write path, no UI change, no new dependency. Sessions already frozen recover automatically via the merge guard; no sidecar migration is included.
- **Evidence needed before claiming done:** a bug-fix test that fails before the fix and passes after; the neighbouring data-loss suites (#2914, #3831, #4767) still green; a full-suite A/B against pristine `HEAD`; and an end-to-end check through the real display path on a live session.

## Release note

Sessions could stop rendering new messages after compression and silently drop later turns from the transcript. A wall-clock fallback in the truncation-watermark advance helper created a self-locking filter that hid the very `state.db` rows needed to unstick the merge. The advance helper now only ever advances to a real message timestamp, and the merge ignores an impossible (newer-than-every-row) watermark and fails open toward data.

Not verified: I could not exercise the WebUI HTTP API directly because it requires authentication, so end-to-end evidence uses the display-merge function the browser path calls rather than a live request.

