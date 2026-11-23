You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

update_spec and create_table accept two partition fields with the same name

### Apache Iceberg version

main (development)

### Please describe the bug 🐞

`validate_partition_name` in `pyiceberg/partitioning.py` is meant to reject empty and duplicate partition field names (`Partition name has to be unique: ...`), but it returns early when the name is not also a schema column, so those checks only run for names that match a column. As a result `update_spec()` can commit a spec with two fields of the same name, for example through `rename_field`. `create_table` does not check uniqueness at all, because `assign_fresh_partition_spec_ids` passes a fresh set of names for every field.

```python
from pyiceberg.catalog.sql import SqlCatalog
from pyiceberg.schema import Schema
from pyiceberg.transforms import BucketTransform
from pyiceberg.types import LongType, NestedField

catalog = SqlCatalog("default", uri="sqlite:///:memory:", warehouse="file:///tmp/warehouse")
catalog.create_namespace("db")
schema = Schema(NestedField(1, "x", LongType()), NestedField(2, "y", LongType()))
table = catalog.create_table("db.events", schema)

with table.update_spec() as update:
    update.add_field("x", BucketTransform(16), "x_bucket")
    update.add_field("y", BucketTransform(16), "y_bucket")

with table.update_spec() as update:
    update.rename_field("x_bucket", "y_bucket")  # accepted

print(table.spec())
```

Output on main:

```
[
  1000: y_bucket: bucket[16](1)
  1001: y_bucket: bucket[16](2)
]
```

Expected: `ValueError: Partition name has to be unique: y_bucket`, as when the name matches a schema column.

### Willingness to contribute

- [x] I can contribute a fix for this bug independently

