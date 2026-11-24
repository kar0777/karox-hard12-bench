You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

A copied sidecar whose body names another session overwrites that session's conversation on its first load

## Summary

`Session.load(sid)` collapses adjacent duplicate `_partial` rows and then calls `session.save(touch_updated_at=False, skip_index=True)` (`api/models.py`, `Session.load`, the `if _collapsed_partials:` branch). `save()` writes `SESSION_DIR / f"{self.session_id}.json"`, and `self.session_id` comes from the file's **body**, not from the `sid` that was loaded.

So a sidecar whose body names a different session (for example `copy.json` containing `"session_id": "victim"`) and has duplicate partials **overwrites `victim.json` with its own transcript and profile** the first time anything loads it. `copy.json` itself is left unchanged.

No request is needed. Listing sessions with the index missing rebuilds it, and the rebuild loads the copy.

## Reproduced (v0.52.544 and exp-v0.52.638)

The setup is a `victim-8834.json` with 5 turns and profile `work`, plus a `copy-8834.json` whose body says `"session_id": "victim-8834"`, profile `default`, holding `[user, partial, partial]`.

| trigger | victim before | victim after | `victim.json.bak` |
|---|---|---|---|
| `Session.load("copy-8834")` | 5 rows, `work` | 2 rows, `default` | 5 rows |
| `all_sessions()` with no `_index.json` (no request) | 5 rows | 2 rows | 5 rows |
| 3 repeated loads of the copy | 5 rows | 2 rows each time | still 5 rows |

The original transcript survives only in the single `.bak` generation. A later shrinking save of `victim` replaces it.

## Fix shape

Persist the collapse only when the body names the file being loaded:
- if `session.session_id != sid`, keep the in-memory collapse, skip the save, and log it;
- if the body has no `session_id` at all, `Session(**data)` generates a random id, so skip the save in that case too.

This is the same rule #8833 applied to its share-field repair: a repair writes the record that was asked for, never an id read from the record's own body.

## Scope and related

- **Trigger:** a sidecar whose filename stem differs from its body `session_id`, e.g. a manual copy or a backup restored under another name. Sync-conflict copies usually aren't affected: their names contain dots or spaces, which `is_safe_session_id` rejects.
- **#8834:** separate from #8834 (refused requests still run this save). #8834's fix keeps the three refusing routes from loading such a file (unverifiable ownership fails closed, as in #8094), but background loads still reach this save.
- **Write paths:** this is the only write this probe found. Other derived writes keyed by the body id (index rows) were not checked here.

