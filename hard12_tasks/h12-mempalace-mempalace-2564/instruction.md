You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

sync --apply removes a drawer when a volume mounted over its directory carries a same-named file and a .gitignore naming it

**What happened?**

`sync --apply` removes a drawer whose source file is on disk the whole time, when a volume mounted over the file's directory carries a file of the same name and a `.gitignore` naming it. The `gitignored` verdict comes from one reading of the path, and nothing in it says whose directory answered. The `missing` verdict beside it asks, since #2368, and keeps the neighbour.

Measured on `develop` @ e038af97 through the real CLI, with real `mount` and `umount` inside `unshare --mount --map-root-user`, one run each: two files mined from `proj/data`, one drawer each, then a tmpfs over `proj/data`.

| what the volume carries | `sync proj --apply` reports | removed |
|---|---|---|
| a `notes.md` of its own and a `.gitignore` saying `notes.md` | `Gitignored: 1 (removed)`, `Unresolved: 1 (kept)` | `notes.md`'s drawer; `other.md`'s is kept by its recorded identity |
| the same `notes.md`, no `.gitignore` | `Unresolved: 1 (kept)` | nothing |
| neither file | `Unresolved: 2 (kept)` | nothing |
| eight files named like eight mined ones, and a `.gitignore` saying `*` | `Gitignored: 8 (removed)` | every drawer; the palace goes from eight sources to none |

After the unmount both files are back on disk, and a search for `notes.md`'s words answers with `other.md`'s paragraph until a re-mine.

**What did you expect?**

The `gitignored` verdict read like the `missing` one: a drawer carrying the identity `source_identity` records is removed only when the directory answered with that inode before and after the rule was read, and is otherwise kept as unresolved. A drawer carrying no identity is decided by the rule alone, and a rule in the project's own tree keeps removing: with no mount and `proj/data/.gitignore` saying `notes.md`, the run reports `Gitignored: 1 (removed)`, `Kept: 1`.

**How to reproduce:**

Inside `unshare --mount --map-root-user`, with `<p>` a scratch palace and `prose` a few lines of text (a one-line file files no drawer).

1. `mkdir -p proj/data && prose > proj/data/notes.md && prose > proj/data/other.md`
2. `mempalace --palace <p> mine proj` reports `Drawers filed: 2`
3. `mount -t tmpfs tmpfs proj/data && echo generated > proj/data/notes.md && echo notes.md > proj/data/.gitignore`
4. `mempalace --palace <p> sync proj --apply` reports `Gitignored: 1 (removed)`, `Unresolved: 1 (kept)`, `Removed 1 drawers, 1 closets`
5. `umount proj/data`: both files are back, and `mempalace --palace <p> mine proj` reports `Drawers filed: 1`.

**Environment:**
- OS: Linux (WSL2)
- Python version: 3.12.3
- MemPal version: `develop` @ e038af97

One of the two reports promised on #2320 once #2367 landed; #2368 names the `gitignored` route as unchanged.

