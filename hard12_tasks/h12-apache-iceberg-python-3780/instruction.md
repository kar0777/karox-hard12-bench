You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

`overwrite().delete_data_file()` fails with non-identity partition transforms (`BucketTransform`) due to manifest-pruning predicate reconstruction (regression vs 0.11.1)

### Apache Iceberg version

main (development)

### Please describe the bug 🐞

Found when running 0.12RC

## Summary

`delete_data_file()` in the overwrite snapshot path crashes when the table partition spec uses a non-identity transform (for example, `BucketTransform` on a `string` source column).

Observed error:
```text
TypeError: Cannot convert LongLiteral into string
```

This appears to be introduced by commit `8a47d2bf` (["Optimization: Prune manifest in snapshot overwrite operations"](https://github.com/apache/iceberg-python/pull/3011)), which added `_SnapshotProducer._build_delete_files_partition_predicate()` and calls it from `_manifests()`.

## Affected API Pattern

This affects the lower-level transactional overwrite path:

```python
with table.transaction() as txn:
    with txn.update_snapshot().overwrite() as ov:
        ov.delete_data_file(existing_file)
```

This does **not** report through the same path as `table.delete(predicate)` / `table.overwrite(df, overwrite_filter=...)`, which operate from user-provided predicates.

## Root Cause

`_SnapshotProducer._build_delete_files_partition_predicate()` groups deleted files by `spec_id` and stores each `data_file.partition` record.

It then calls:

```python
self._transaction._build_partition_predicate(
    partition_records=partition_records,
    schema=self.schema(),
    spec=self.spec(spec_id),
)
```

`Transaction._build_partition_predicate` currently builds `EqualTo(Reference(source_column_name), stored_partition_value)` for each partition field.

That is only valid for `IdentityTransform`, where the stored partition value is the source-column domain value.

For `BucketTransform`, the stored partition value is a bucket id (integer), not the original source value (e.g. `string`). Binding then fails with:

```text
TypeError: Cannot convert LongLiteral into string
```

There is already an explicit identity-only guard in `Transaction.dynamic_partition_overwrite` before using `_build_partition_predicate`; the overwrite delete-data-file call site added in `8a47d2bf` does not have a corresponding guard.

## Reproduction script:
```
from __future__ import annotations

import sys
import traceback
import uuid
from pathlib import Path
from tempfile import TemporaryDirectory

import pyarrow as pa

from pyiceberg.catalog.sql import SqlCatalog
from pyiceberg.partitioning import PartitionField, PartitionSpec
from pyiceberg.schema import Schema
from pyiceberg.transforms import BucketTransform
from pyiceberg.types import IntegerType, NestedField, StringType


def _print_step(step: int, message: str) -> None:
    print(f"\n[{step}] {message}")


def main() -> int:
    _print_step(1, "Creating in-memory SqlCatalog with temp warehouse")
    with TemporaryDirectory(prefix="pyiceberg-bucket-delete-bug-") as tmp_dir:
        warehouse = Path(tmp_dir) / "warehouse"
        warehouse.mkdir(parents=True, exist_ok=True)

        catalog = SqlCatalog(
            "repro",
            uri="sqlite:///:memory:",
            warehouse=f"file://{warehouse}",
        )
        catalog.create_tables()

        namespace = "repro_ns"
        table_name = f"bucket_delete_bug_{uuid.uuid4().hex[:8]}"
        identifier = (namespace, table_name)

        _print_step(2, f"Creating namespace: {namespace}")
        catalog.create_namespace(namespace)

        _print_step(3, "Creating table with bucket partition transform on string column tenant_id")
        schema = Schema(
            NestedField(1, "tenant_id", StringType(), required=True),
            NestedField(2, "value", IntegerType(), required=True),
        )
        spec = PartitionSpec(
            PartitionField(
                source_id=1,
                field_id=1000,
                transform=BucketTransform(8),
                name="tenant_id_bucket",
            ),
            spec_id=0,
        )

        table = catalog.create_table(
            identifier=identifier,
            schema=schema,
            partition_spec=spec,
            properties={"format-version": "2"},
        )

        _print_step(4, "Appending rows so at least one data file exists in the bucketed spec")
        write_df = pa.Table.from_pylist(
            [
                {"tenant_id": "tenant-a", "value": 1},
                {"tenant_id": "tenant-b", "value": 2},
                {"tenant_id": "tenant-c", "value": 3},
            ],
            schema=pa.schema(
                [
                    pa.field("tenant_id", pa.string(), nullable=False),
                    pa.field("value", pa.int32(), nullable=False),
                ]
            ),
        )
        table.append(write_df)

        _print_step(5, "Planning files and selecting one DataFile for delete_data_file()")
        tasks = list(table.scan().plan_files())
        if not tasks:
            print("No data files were planned; repro cannot proceed.")
            return 2

        existing_file = tasks[0].file
        print(f"Selected data file path: {existing_file.file_path}")
        print(f"Selected data file spec_id: {existing_file.spec_id}")
        print(f"Selected data file stored partition record: {existing_file.partition!r}")

        _print_step(
            6,
            "Running transaction overwrite.delete_data_file(existing_file) and expecting TypeError",
        )
        try:
            with table.transaction() as txn:
                with txn.update_snapshot().overwrite() as overwrite:
                    overwrite.delete_data_file(existing_file)
        except TypeError as exc:
            print("\nObserved expected exception:")
            print(f"{type(exc).__name__}: {exc}")
            print("\nFull traceback:")
            traceback.print_exc()
            return 0

        print("No exception was raised. The bug may already be fixed on this checkout.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

### Willingness to contribute

- [x] I can contribute a fix for this bug independently
- [ ] I would be willing to contribute a fix for this bug with guidance from the Iceberg community
- [ ] I cannot contribute a fix for this bug at this time
