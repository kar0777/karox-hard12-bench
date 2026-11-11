You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Three reload-by-id helpers still write the session a copy's body names when handed the copy directly (defense in depth after #8852)

Follow-up to #8852 / #8859. Found by the round-5 Codex gate on #8859 (`e75a5aed3ea8`) and reproduced independently. These gaps are older than #8859 and **no production flow reaches them today**, so this is defense in depth. It isn't a live data-loss path.

## The class

`Session.load(sid)` on a file whose body names another session returns an object marked `_sidecar_names_other_session = sid`. Its `session_id` is the **body** id, which is the other session's id (the "victim").

- **What #8859 guards:** `save()` on the marked object. It also adds explicit refusals in chat/start, `start_session_turn`, the reasoning and workspace writers, startup reattach, and (reviewer commit `e75a5aed3`) `_persist_generated_session_title`.
- **The hole:** a helper that takes the object and then **re-loads or re-resolves by `session.session_id`** gets the victim's own, unmarked object. Saving that bypasses the `save()` guard and writes the victim.

## Three remaining helpers of that class

Each was reproduced by calling it directly with a marked copy object, using the `store` fixtures from `tests/test_issue8852_body_id_write_target.py` (victim + copy, `partials=False`). The victim's messages are unchanged in every case; only these fields are written.

| helper | what lands in the victim's file | production caller and why a copy can't reach it today |
|---|---|---|
| `api/routes.py` `_queue_generated_title_for_imported_session` (~L200; the thread re-loads `Session.load(sid)`) | `title` "CLI Session" becomes the generated title, and `llm_title_generated` goes from false to true | `routes.py` ~L36126 (CLI import) passes the object it just built with `import_cli_session(...)` and saved, so the id matches its own file |
| `api/streaming.py` `_merge_process_wakeup_pause_into_current_session` (~L3523) | `process_wakeup_pause` is stamped (classification, credential fingerprint, ...) | `streaming.py` ~L18488 / ~L18928 run inside a turn, and turn admission (chat/start, `start_session_turn`) 404s a copy since #8859 |
| `api/streaming.py` `_preserve_pre_compression_snapshot` (~L7595) | the pre-compression snapshot and continuation fields are stamped | `streaming.py` ~L7751 runs only after `SESSIONS.get(old_sid) is s and s.session_id == old_sid`; a copy is cached under its file name, so the migration is blocked first |

## Fix shape

Do the same as `e75a5aed3`. Each helper refuses a marked object before it resolves or re-loads anything:
- the import-title queue returns before extracting the id;
- the wakeup-pause merge returns `None`;
- the compression snapshot returns `False`.

Add one test per helper, modelled on `test_the_title_writer_refuses_a_session_loaded_from_a_copy`. Each must be red without its guard.

**Root option, bigger:** a single helper (e.g. `_refuse_session_loaded_from_copy(session)`) used by every reload-by-id writer. Or stop handing out marked objects whose `session_id` is the body id. That is a design change to #8859's marking approach, so it belongs in its own PR.

