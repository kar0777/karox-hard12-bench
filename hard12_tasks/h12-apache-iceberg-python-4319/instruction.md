You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

`create_branch` and `create_tag` replace an existing ref of the same name

### Apache Iceberg version

0.12.0 (latest release)

### Please describe the bug 🐞

Currently, `create_branch` and `create_tag` set the ref without checking whether it exists, so an existing branch is reset and loses its commits, and a tag moves. Java refuses an existing name with `Ref dev already exists`.

```python
import tempfile
import pyarrow as pa
from pyiceberg.catalog.sql import SqlCatalog

cat = SqlCatalog("c", uri="sqlite:///:memory:", warehouse=f"file://{tempfile.mkdtemp()}")
cat.create_namespace("ns")
t = cat.create_table("ns.t", schema=pa.schema([("x", pa.int64())]))
t.append(pa.table({"x": [1]}))
s1 = t.current_snapshot().snapshot_id
t.manage_snapshots().create_branch(s1, "dev").create_tag(s1, "v1").commit()
t.append(pa.table({"x": [2]}), branch="dev")
t.append(pa.table({"x": [3]}))

t.manage_snapshots().create_branch(s1, "dev").commit()
print(t.scan().use_ref("dev").to_arrow()["x"].to_pylist())
# [1], should raise; the commit holding 2 is now on no ref

t.manage_snapshots().create_tag(t.current_snapshot().snapshot_id, "v1").commit()
print(sorted(t.scan().use_ref("v1").to_arrow()["x"].to_pylist()))
# [1, 3], should raise and leave v1 at [1]
```

`remove_branch` and `remove_tag` check nothing either: `remove_branch("main")` is accepted and the table then reads as empty.

tested on pyiceberg 0.12.0 and main

### Willingness to contribute

- [ ] I can contribute a fix for this bug independently
- [ ] I would be willing to contribute a fix for this bug with guidance from the Iceberg community
- [ ] I cannot contribute a fix for this bug at this time
