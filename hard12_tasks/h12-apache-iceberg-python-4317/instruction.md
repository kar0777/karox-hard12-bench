You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

A retried transaction validates a write on one branch against another branch's commits

### Apache Iceberg version

main (development)

### Please describe the bug 🐞

On retry, `Transaction._rebuild_snapshot_updates` resolves a single `CommitWindow` from the first snapshot producer's
branch and starting snapshot, then uses it for every producer:

```python
starting_id = self._snapshot_producers[0]._starting_snapshot_id if self._snapshot_producers else None
target_branch = self._snapshot_producers[0]._target_branch if self._snapshot_producers else None
commit_window = CommitWindow.resolve(self._table.metadata, starting_id, target_branch)

for producer in self._snapshot_producers:
    producer._commit_window = commit_window
```

In a transaction that writes more than one branch, a validating producer (`delete`/`overwrite`) on a later branch is
checked against the first branch's commits. If the first branch didn't change, the window is empty and validation is
skipped, so a serializable delete commits over a conflicting concurrent append it never saw.

**Blocked by #4315** (fix for #4183). Before that fix, the second branch's `AssertRefSnapshotId` was dropped, so the
conflict never triggered a retry and this path was unreachable; #4315 is what exposes it. I'm not folding this into
#4315, to keep that PR scoped to #4183, but I'm willing to work on this one and will open a PR on top of #4315 once it
lands.

```python
import tempfile
import pyarrow as pa
from pyiceberg.catalog.sql import SqlCatalog

cat = SqlCatalog("c", uri="sqlite:///:memory:", warehouse=f"file://{tempfile.mkdtemp()}")
cat.create_namespace("ns")
t = cat.create_table("ns.t", schema=pa.schema([("x", pa.int64())]),
                     properties={"commit.retry.min-wait-ms": "1", "commit.retry.max-wait-ms": "2"})
t.append(pa.table({"x": [0, 1]}))
t.manage_snapshots().create_branch(t.current_snapshot().snapshot_id, "b").commit()

tx = t.transaction()
tx.append(pa.table({"x": [9]}))          # remove this line and the commit below raises ValidationException
tx.delete("x == 1", branch="b")
cat.load_table("ns.t").append(pa.table({"x": [1]}), branch="b")   # concurrent matching append to b
tx.commit_transaction()
# commits; should raise ValidationException like the single-branch delete does
print(sorted(cat.load_table("ns.t").scan().use_ref("b").to_arrow()["x"].to_pylist()))   # [0, 1]
```

Tracing `CommitWindow.resolve` shows the retry resolving `branch='main'` (empty window) for the delete on `b`. Without
the `main` append, it resolves `branch='b'` (non-empty) and validation raises.

Resolving a window per producer from its own `_starting_snapshot_id` and `_target_branch` would scope the validation
correctly.

tested on main with #4315 applied

### Willingness to contribute

- [x] I can contribute a fix for this bug independently
- [ ] I would be willing to contribute a fix for this bug with guidance from the Iceberg community
- [ ] I cannot contribute a fix for this bug at this time

