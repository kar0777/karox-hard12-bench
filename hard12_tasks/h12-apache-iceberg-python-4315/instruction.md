You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

A transaction writing two branches overwrites concurrent changes to the second

### Apache Iceberg version

0.12.0 (latest release)

### Please describe the bug 🐞

Currently, `Transaction._stage` drops a requirement whose type is already staged, so a transaction writing two branches sends `AssertRefSnapshotId` for the first only, and a concurrent change to the second is overwritten. With `main` written first, a concurrent rollback of `main` is caught and retried.

```python
import tempfile
import pyarrow as pa
from pyiceberg.catalog.sql import SqlCatalog

cat = SqlCatalog("c", uri="sqlite:///:memory:", warehouse=f"file://{tempfile.mkdtemp()}")
cat.create_namespace("ns")
row = lambda x: pa.table({"x": [x]})
t = cat.create_table("ns.t", schema=row(1).schema)
t.append(row(1))
s1 = t.current_snapshot().snapshot_id
t.append(row(2))
t.manage_snapshots().create_branch(t.current_snapshot().snapshot_id, "b").commit()

cat.load_table("ns.t").manage_snapshots().rollback_to_snapshot(s1).commit()
with t.transaction() as tx:
    tx.append(row(3), branch="b")
    tx.append(row(3))
print(sorted(cat.load_table("ns.t").scan().to_arrow()["x"].to_pylist()))
# [1, 2, 3], should be [1, 3]
# another writer rolled main back to [1] after t was loaded, and this commit put 2 back
```

On a format-version 1 table, another writer's append to `main` is lost the same way.

tested on pyiceberg 0.12.0 and main

### Willingness to contribute

- [ ] I can contribute a fix for this bug independently
- [ ] I would be willing to contribute a fix for this bug with guidance from the Iceberg community
- [ ] I cannot contribute a fix for this bug at this time
