You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

A session file swapped mid-turn makes the write resolver return the other session; an ephemeral cancel then deletes its file

The session-write resolver checks the session object it is given, not the one it hands back. If a session's own file is replaced mid-turn with a copy of another session's file, the resolver returns that copy-loaded object, and an ephemeral cancel then deletes the **other** session's file.

Found while gating #8949 (which fixes #8869). It is pre-existing: the same probe gives the same result on master and on #8949's stage, so it isn't caused by #8949 and doesn't block it.

## Where

`api/streaming.py`, `_resolve_current_session_for_write` (master `exp-v0.52.666`, `356872452547`, line 3505). #8949 adds a guard on the input object; the object it returns from `get_session(sid)` isn't checked.

Two callers use the returned object:
- **Turn-end cwd mirror:** targets the returned session's `state.db` row.
- **Cancel finalizer:** `_finalize_cancelled_turn(..., ephemeral=True)` calls `_cleanup_ephemeral_cancelled_turn`, which runs `pathlib.Path(session.path).unlink(missing_ok=True)` (line 3500) on the returned object. Its `path` is the other session's file.

## Reproduction

The probe is a throwaway pytest file that reuses the store fixtures in `tests/test_issue8852_body_id_write_target.py`. I ran it in a network-less sandbox with the Agent venv.

1. Save session `own-8949`, then load it as the worker's snapshot.
2. Overwrite `own-8949.json` with the JSON of session `victim-8852` (the body names `victim-8852`), then clear `SESSIONS`.
3. `_resolve_current_session_for_write(snapshot)` returns an object with `session_id == "victim-8852"` and `_sidecar_names_other_session == "own-8949"`. The cwd mirror would target `victim-8852`.
4. Register the writeback owner for `own-8949`, then call `_finalize_cancelled_turn(snapshot, ephemeral=True, stream_id=...)`. Afterwards `victim-8852.json` no longer exists.

Result, identical on master `356872452547` and on #8949's stage `26e579949816`:

```
PROBE resolver-output: returned_id= victim-8852 marked= own-8949
PROBE cwd-mirror target id = victim-8852
PROBE ephemeral-finalize: victim file exists after = False
```

## How likely

It needs an outside writer to replace a session's file with a copy of another session's while a turn is running, for example a backup restored over an existing file, or a manual copy. That's unlikely, but the result is the other conversation's file deleted, and it breaks the invariant #8852, #8859 and #8869 set out to hold.

## Fix shape

Refuse a marked object on the way out as well as on the way in:

```python
current = get_session(sid)
if getattr(current, "_sidecar_names_other_session", None):
    return None
return current
```

The reviewer checked that this closes both cases (the cwd mirror skips the write, and the finalizer returns without deleting), and that 48 neighbouring tests still pass. A regression test can reuse the probe above.

