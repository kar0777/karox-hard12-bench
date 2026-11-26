You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Correcting or deleting a drawer never invalidates its closets, and no verb can rebuild them

Closets are derived from a source file at mine time and are only ever rebuilt by re-mining that file. No drawer-mutation path touches them. So a drawer that is corrected in place keeps a closet that quotes the pre-correction text, indefinitely, and there is no way to fix it short of re-mining a file that may no longer exist.

This bites hardest on retraction: the one case where the old text is not merely stale but actively harmful, because it reads as a live instruction.

## Why it happens

Closets are built from the **file content**, not from the stored drawers:

- `build_closet_lines(source_file, drawer_ids, content, wing, room)` — `mempalace/palace.py:133`, called at `mempalace/miner.py:632` with the mined file's `content`.
- They are replaced only by `purge_file_closets` + `upsert_closet_lines` (`mempalace/palace.py:191` and `:204`), keyed on `source_file`. Every caller is a mine/ingest path: `miner.py:647-648`, `closet_llm.py:283-284`, `diary_ingest.py:181-182`.

Neither drawer-mutation tool goes near the closets collection:

- `tool_update_drawer` — `mempalace/mcp_server.py:798`. Rewrites the drawer document and metadata via `col.update(...)`. No closet call.
- `tool_delete_drawer` — `mempalace/mcp_server.py:694`. Deletes the drawer. No closet call.

The only `closet` references in `mcp_server.py` are the KG's `source_closet` provenance field (`:883`, `:900`, `:904`, `:1271`), which is unrelated.

Writing to Chroma directly has the same result, for the same reason.

## Reproduction

```
1. Mine a file whose text contains a queued instruction.
   -> drawer_<wing>_<room>_<id>   "TODO next session: <instruction>"
   -> closet_<wing>_<room>_<id>_01 contains a topic line quoting it

2. The task gets done. Retract the drawer in place:
   mempalace_update_drawer(drawer_id, content="[RETRACTED - COMPLETE. DO NOT ACT ON THIS.] ...")

3. Search for the instruction.
   The drawer is corrected. The closet still quotes the withdrawn text verbatim.
```

Step 3 has no remedy in the CLI: `init | mine | search | compress | wake-up | status | doctor | repair`. Re-mining is the only rebuild path, and it needs the original `source_file` — which for a drawer filed from a session handoff, a scratch path, or any synthetic source no longer exists.

## Impact

In `search_memories`, a stale closet is not inert. Per `mempalace/searcher.py:342-363`, closets contribute a **rank boost keyed by `source_file`** plus a `cdoc[:200]` **preview string** lifted straight from the closet document. So the withdrawn text can both promote its own source's drawers and be shown verbatim in the result preview.

It is worse for anything that mirrors the closets collection as first-class searchable documents rather than as a ranking signal. I hit this building a BigQuery mirror: after correctly retracting a drawer and propagating the correction, a semantic search for the withdrawn instruction returned the **stale closet as the single highest-ranked result**, at 0.797 similarity — well above the corrected drawer. The retraction was complete and correct at the drawer layer and completely undone one layer up.

## Secondary: pointers outlive their drawers

Closet topic lines embed `→drawer_id_a,drawer_id_b` references. `tool_delete_drawer` removes the drawer without touching them, so those pointers dangle with nothing to detect or repair it. Low severity today — `_extract_drawer_ids_from_closet` (`searcher.py:146`) is defined but has no callers, so nothing currently resolves them — but it is the same root cause and will matter as soon as something does.

## Possible directions

Roughly in order of cost:

1. **Invalidate on mutation.** Have `tool_update_drawer` / `tool_delete_drawer` mark the affected `source_file`'s closets stale, and have search skip or de-boost stale closets. Cheap, and it makes the failure fail safe rather than silently.
2. **A rebuild verb.** `mempalace compress --rebuild <source_file|wing/room>` that regenerates closets from the **stored drawers** instead of the source file. This also closes the "source file is gone" hole, which no re-mine can.
3. **Propagate the retraction.** On update, re-derive just the affected topic lines from the new drawer text. Most correct, most work, and needs a defined story for line-to-drawer attribution.

(1) plus (2) would have been enough here: the retraction would have been visible to the closet layer, and there would have been a way to act on it.

Related in kind, though a different mutation: #1938 (wing-name migration re-keys drawers but leaves hallways/tunnels on the old wing). Same shape — a mutation path that leaves a derived layer pointing at the old world.

