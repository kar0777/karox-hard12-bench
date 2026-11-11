You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

dbt docs generate emits RuntimeWarning "does not match the name of any column" for comment, table_owner, table_comment

### Describe the bug
`dbt docs generate` emits a flood of agate `RuntimeWarning`s while building the catalog:

```
agate/type_tester.py:92: RuntimeWarning: "comment" does not match the name of any column in this table.
agate/type_tester.py:92: RuntimeWarning: "table_owner" does not match the name of any column in this table.
agate/type_tester.py:92: RuntimeWarning: "table_comment" does not match the name of any column in this table.
```

In a single run against a project with ~460 models the output contained 52x `comment`, 51x `table_owner` and 11x `table_comment`. The catalog is still written correctly; this is log noise, but it is large.

The cause is in `DatabricksAdapter._get_schema_for_catalog` (introduced by #1428 for #1392):

1. `CATALOG_TEXT_ONLY_COLUMNS` is passed to `build_type_tester` whenever `columns` is non-empty.
2. The rows come from `_get_columns_for_catalog`, which uses `column.to_column_dict()`. In dbt-spark that defaults to `omit_none=True`, so keys whose value is `None` are dropped.
3. `comment` is never set on this code path, and `table_owner` / `table_comment` are `None` for relations without an owner or table comment. A schema where no row carries one of those keys ends up with a table that has no such column.
4. agate's `TypeTester` warns once for every forced column name that is missing from the table.

#1428 handled the case of a completely empty schema (0-column table), but not rows that are present and only partially keyed.

### Steps To Reproduce
Run `dbt docs generate` on a project where at least one schema has relations with no table comment/owner. The existing unit-test helper `_catalog_row` hides this because it includes `"comment": None`, whereas real rows omit None-valued keys. Removing `table_owner`, `table_comment` and `comment` from the row and running `_get_schema_for_catalog` under `warnings.simplefilter("error", RuntimeWarning)` reproduces it.

### Expected behavior
No `RuntimeWarning`s. Only the metadata columns that are actually present in the rows need to be force-typed as Text (which is what #1392 requires).

### System information
**The output of `dbt --version`:**
```
dbt-core 1.12.0
dbt-databricks 1.12.3
```
The catalog code is identical on 1.12.8.

**The operating system you're using:** Databricks Runtime 17.3 (Linux), dbt task on a job cluster

**The output of `python --version`:** 3.12.3

### Additional context
I have a small fix and a unit test ready and will open a PR that references this issue.

