You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Partition-scoped position deletes are not applied in NaN identity partitions

### Apache Iceberg version

0.12.0 (latest release)

### Please describe the bug 🐞

Scans can return deleted rows with no error on tables written by Spark or Java. This happens in a NaN identity partition when a position delete file covers more than one data file.

I reproduced the scan failure on 0.12.0 and main at `e3564a54c10960307147377c578680276865ed18`, with Python 3.12 and PyArrow 25.0.1 on Linux/amd64. The same script returns the correct rows on 0.10.0. The bug affects 0.11.0 and later.

The reproduction uses synthetic data in a v2 table identity-partitioned on a `double` column. Each partition, `1.0` and NaN, has two data files. One position delete file per partition deletes position 0 from both data files, without `file_path` bounds. Because PyIceberg cannot write delete files, the script writes the Parquet files with PyArrow and commits them through `fast_append()` and a small delete-manifest writer, in the shape that Spark or Java would produce.

Install `pyiceberg[pyarrow,sql-sqlite]==0.12.0` and `pyarrow==25.0.1`. The script runs unchanged on main and 0.10.0.

```python
import os
import tempfile

import pyarrow as pa
import pyarrow.parquet as pq

from pyiceberg.catalog.sql import SqlCatalog
from pyiceberg.manifest import DataFile, DataFileContent, FileFormat, ManifestContent, ManifestWriterV2
from pyiceberg.partitioning import PartitionField, PartitionSpec
from pyiceberg.schema import Schema
from pyiceberg.transforms import IdentityTransform
from pyiceberg.typedef import Record
from pyiceberg.types import DoubleType, IntegerType, NestedField

a, b = Record(float("nan")), Record(float("nan"))
print(f"Record(nan) == Record(nan): {a == b}; hashes equal: {hash(a) == hash(b)}")

warehouse = tempfile.mkdtemp()
catalog = SqlCatalog("default", uri=f"sqlite:///{warehouse}/catalog.db", warehouse=f"file://{warehouse}")
catalog.create_namespace("default")
schema = Schema(NestedField(1, "id", IntegerType()), NestedField(2, "value", DoubleType()))
spec = PartitionSpec(PartitionField(source_id=2, field_id=1000, transform=IdentityTransform(), name="value"))
tbl = catalog.create_table("default.t", schema=schema, partition_spec=spec, properties={"format-version": "2"})

pos_delete_schema = pa.schema(
    [
        pa.field("file_path", pa.string(), nullable=False, metadata={"PARQUET:field_id": "2147483546"}),
        pa.field("pos", pa.int64(), nullable=False, metadata={"PARQUET:field_id": "2147483545"}),
    ]
)


def write_file(name: str, rows: pa.Table, value: float, content: DataFileContent) -> DataFile:
    path = f"{warehouse}/{name}.parquet"
    pq.write_table(rows, path)
    return DataFile.from_args(
        content=content,
        file_path=path,
        file_format=FileFormat.PARQUET,
        partition=Record(value),
        record_count=rows.num_rows,
        file_size_in_bytes=os.path.getsize(path),
    )


class DeleteManifestWriter(ManifestWriterV2):
    def content(self) -> ManifestContent:
        return ManifestContent.DELETES

    @property
    def _meta(self) -> dict[str, str]:  # private: the manifest header names its content
        return {**super()._meta, "content": "deletes"}


# Write files the way Spark or Java would: PyIceberg 0.12 cannot append to a NaN partition, and PyIceberg
# cannot write delete files. Each partition gets two data files and one position delete file that removes
# row 0 of both. A delete file covering two data files has no file_path bounds, so it is partition-scoped.
data_files, delete_files = [], []
for value, ids in [(1.0, [1, 2, 3, 4]), (float("nan"), [5, 6, 7, 8])]:
    for pair in (ids[:2], ids[2:]):
        rows = pa.Table.from_pydict({"id": pair, "value": [value] * 2}, schema=schema.as_arrow())
        data_files.append(write_file(f"data-{pair[0]}", rows, value, DataFileContent.DATA))
    deletes = pa.Table.from_pydict({"file_path": [f.file_path for f in data_files[-2:]], "pos": [0, 0]}, schema=pos_delete_schema)
    delete_files.append(write_file(f"deletes-{ids[0]}", deletes, value, DataFileContent.POSITION_DELETES))

with tbl.transaction() as tx, tx.update_snapshot().fast_append() as append:
    for data_file in data_files:
        append.append_data_file(data_file)

with tbl.transaction() as tx, tx.update_snapshot().overwrite() as overwrite:
    # private: PyIceberg has no delete-manifest writer, so swap one into the snapshot producer
    overwrite.new_manifest_writer = lambda spec: DeleteManifestWriter(
        spec, tbl.schema(), overwrite.new_manifest_output(), overwrite._snapshot_id, "deflate"
    )
    for delete_file in delete_files:
        overwrite.append_data_file(delete_file)

print("expected ids:", [2, 4, 6, 8])
print("actual ids:  ", sorted(tbl.scan().to_arrow()["id"].to_pylist()))
```

Output on main and 0.12.0:

```text
Record(nan) == Record(nan): False; hashes equal: True
expected ids: [2, 4, 6, 8]
actual ids:   [2, 4, 5, 6, 7, 8]
```

The `1.0` partition is correct in every tested version. Version 0.10.0 returns the correct rows in both partitions, even though `Record` equality already fails for NaN there. I also checked per-file position deletes with equal `file_path` bounds separately on main. They work in both partitions, but that control is not included in this script.

[`DeleteFileIndex`](https://github.com/apache/iceberg-python/blob/e3564a54c10960307147377c578680276865ed18/pyiceberg/table/delete_file_index.py#L115-L137) looks up partition-scoped deletes by `(spec_id, Record)`. [`Record.__eq__`](https://github.com/apache/iceberg-python/blob/e3564a54c10960307147377c578680276865ed18/pyiceberg/typedef.py#L198-L200) compares lists, so separately decoded NaN partition values compare unequal even though their hashes match. A narrow fix would compare NaN partition values as equal, as Java does through [`StructLikeWrapper`](https://github.com/apache/iceberg/blob/5a2ccf5ba830838ecf182bccb516d5ee48f8b8ed/core/src/main/java/org/apache/iceberg/util/StructLikeWrapper.java#L74-L104) and the [float and double comparators](https://github.com/apache/iceberg/blob/5a2ccf5ba830838ecf182bccb516d5ee48f8b8ed/api/src/main/java/org/apache/iceberg/types/Comparators.java#L35-L41).

The same partition lookup also misses in commit validation, in `_validate_data_files_exist` and `_validate_no_new_deletes_for_data_files`. With the fix for https://github.com/apache/iceberg-python/issues/4277 applied, one writer can replace a data file with a copy while another writer adds a partition-scoped delete for a row in it. The replacement commits and brings the deleted row back for good.

Today, main fails earlier with `ValueError: Cannot create expression literal from NaN`, before reaching those checks. A separate required-files check still rejects replacement of a concurrently removed data file.

Java's [default delete granularity is partition](https://github.com/apache/iceberg/blob/5a2ccf5ba830838ecf182bccb516d5ee48f8b8ed/core/src/main/java/org/apache/iceberg/TableProperties.java#L429-L430). [`PositionDeleteWriter.metrics()`](https://github.com/apache/iceberg/blob/5a2ccf5ba830838ecf182bccb516d5ee48f8b8ed/core/src/main/java/org/apache/iceberg/deletes/PositionDeleteWriter.java#L124-L131) removes the path bounds when a delete file covers multiple data files. Spark writes this shape by default with Iceberg releases before 1.8.0 and with the Spark 3.4 and earlier runtimes. Spark 3.5 and later switched to file granularity in [Iceberg 1.8.0](https://github.com/apache/iceberg/commit/c0d6d42a55a7d33d7d38f73d00e46e86b57d934e). Any Spark version writes it with `write.delete.granularity=partition`.

Related:

- https://github.com/apache/iceberg-python/pull/2918 introduced the partition-keyed index, first released in 0.11.0.
- https://github.com/apache/iceberg-python/pull/3285 is open and would key equality deletes by the same partition `Record`.
- https://github.com/apache/iceberg-python/issues/4277 blocks NaN-partition rewrites on main, so its fix needs to account for the validation failure described here.

I have not run Spark or Java, or tested 0.11.x directly. Java's NaN comparison is based on source inspection.

### Willingness to contribute

- [ ] I can contribute a fix for this bug independently
- [x] I would be willing to contribute a fix for this bug with guidance from the Iceberg community
- [ ] I cannot contribute a fix for this bug at this time

