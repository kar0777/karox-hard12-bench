You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

status cold-loads the HNSW vector index just to count drawers (~60s/call on large palaces)

## What happens

On a large palace (~398k drawers, ~3.5 GB `chroma.sqlite3`), `mempalace status` takes **~60s of CPU on every call**. `mempalace repair-status` returns the same drawer counts in **<1s**.

## Why

`miner.status()` → `_open_collection_or_explain()` → `get_collection()` opens the ChromaDB collection, which **cold-loads the ~586 MB HNSW vector index into memory** — purely to tally drawers by wing/room. But wing/room are plain `embedding_metadata` rows; the relational tables already hold everything `status` needs, and the vector index is never queried.

## Reproduce

```
time mempalace status   # on a palace with hundreds of thousands of drawers
```

## Expected

A metadata-only inspection command should not pay the vector-index load cost. Counts should come from `chroma.sqlite3` directly — the way `repair-status` and `mcp_server._tool_status_via_sqlite` already do.

## Proposed fix

Read the wing/room histogram directly from `chroma.sqlite3`, falling back to the ChromaDB path when the sqlite read is unavailable (missing DB, un-bootstrapped collection, sustained writer lock, unexpected schema). Measured ~60s → ~1s CPU. PR to follow.
