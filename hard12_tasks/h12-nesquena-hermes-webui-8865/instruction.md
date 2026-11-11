You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Deleting a shared conversation leaves its public link live; a share racing the delete brings the conversation back

## Summary

A conversation's public share link outlives the conversation. There are two paths.

**1. Deleting a shared conversation never revokes its share (no race needed).**
- `/api/session/delete` (`api/routes.py` ~20407–20592) removes the sidecar, its `.json.bak` and the draft, but never touches the share snapshot.
- `load_share()` (`api/shares.py:1156`) serves any snapshot without `revoked_at`, and never checks that the session still exists or still holds that token.
- The client's delete flows don't revoke first: `deleteSession` (`static/sessions.js` ~12401) and the batch delete (~6260).
- Once the conversation is gone from the sidebar, there is no UI left to stop sharing it.

**2. A share racing a delete brings the conversation back.**
- `/api/share/create` resolves the session, then `_persist_share_fields` (`api/routes.py:7171`) runs under the persist lock.
- When the sidecar is missing, it falls back to `session.save()` (~7194). That fallback is meant for a pure external session that never had a sidecar, but it also fires for a sidecar a concurrent delete just removed.
- The save rewrites the whole in-memory session, with the new token, plus its index row. The share snapshot is written as well.
- Delete holds the session's agent lock; share create holds the share lock and the persist lock. Neither excludes the other.
- `/api/share/revoke` takes the same fallback with a null token, so it would bring the conversation back unshared. That's from reading the code; I didn't reproduce it separately.

## Reproduced

Driven through the real handlers on an owned session, with share snapshots in a temp dir.

| path | trees | result |
|---|---|---|
| share, then delete | v0.52.544, exp .632 | delete 200; sidecar and index row gone; `load_share(token)` **still serves the conversation** (2 messages) |
| share create paused before persisting, delete runs to completion, then share resumes | exp .632, PR #8833 head `f32f9b2df17a` | delete 200; share 200; **sidecar and index row are back with the new token**, and the public snapshot is live |

This is on stable v0.52.544, so it isn't a regression in the current range. It's older than #8830/#8833. The second path turned up in #8833's writer census as a pre-existing writer, and #8833 doesn't change it.

## Fix shape

- **Bind public serving to a live session.** `load_share` refuses a snapshot unless its session's sidecar exists and still carries that `share_token`. A metadata-prefix read is enough. This also closes the links that past deletes have already orphaned; a fix in delete alone would leave every one of those live.
- **Delete revokes.** Under the session's locks, read the token from the sidecar before unlinking, then `revoke_share` it. That keeps the snapshot store consistent.
- **Share create/revoke must not recreate a deleted session.**
  - Take the session's agent lock (the lock delete holds) around the resolve-and-persist, or re-check existence under it.
  - Limit the `session.save()` fallback to genuinely external sessions that never had a WebUI sidecar, not to "the sidecar is missing".

Related: #8830 / #8833 (the writer census that turned up path 2), and #8834 (another write to a session the request shouldn't touch).

