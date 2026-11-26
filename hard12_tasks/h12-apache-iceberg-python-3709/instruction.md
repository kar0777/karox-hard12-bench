You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

SqlCatalog table operations should filter on `iceberg_type`

### Feature Request / Improvement

In #3263, the `iceberg_type` column was added to the SQLCatalog and filters it in `list_tables`, but the other table operations (i.e. load_table, drop_table, rename_table, commit_table) don't check it yet. That means a view row written by iceberg java or iceberg-rust can bleed in pythons SQLCatalog table operations.

Java's V1 catalog applies `WHERE (iceberg_type = 'TABLE' OR iceberg_type IS NULL)` everywhere ([JdbcUtil.java#L168](https://github.com/apache/iceberg/blob/main/core/src/main/java/org/apache/iceberg/jdbc/JdbcUtil.java#L168)). We should do the same.

Probably worth extracting a small helper since the predicate would now appear in ~5+ places.

Repro steps:

```python
catalog = SqlCatalog("test", uri="sqlite:///...", warehouse="...")
catalog.create_namespace("ns")

# bypass and sim java/rust writing a view row
with catalog.engine.connect() as conn:
    conn.execute(text(
        "INSERT INTO iceberg_tables VALUES "
        "('test', 'ns', 'a_view', 's3://fake/m.json', NULL, 'VIEW')"
    ))
    conn.commit()

catalog.drop_table(("ns", "a_view"))  # Silently deletes the view row :/
```
