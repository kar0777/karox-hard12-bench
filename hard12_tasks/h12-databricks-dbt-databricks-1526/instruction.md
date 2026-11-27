You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

View column tags not applied on the ALTER update path (view_update_via_alter: true) → "main is not being called" error

### Describe the bug

A Unity Catalog view configured with `view_update_via_alter: true` and column-level `databricks_tags` fails on a subsequent `dbt run` whose only change is its column tags, with:

```
Runtime Error in model <model> (models/<model>.sql)
  main is not being called during running model
```

The create path applies column tags correctly; only the `ALTER` update path is affected.

### Steps to reproduce

1. `use_materialization_v2: true`, and the model configured with `+view_update_via_alter: true`.
2. A view model with column-level `databricks_tags` on a column.
3. `dbt run` — the view is created and the tags are applied. ✅
4. Change only the column tags (e.g. add a tag to another column), then `dbt run` again. ❌

### Expected behavior

The changed column tags are applied to the view on the `ALTER` update path, matching the create path and the `table` / V2 materialization paths.

### Actual behavior

`dbt run` errors with `main is not being called during running model`.

### Root cause

`databricks__alter_view` (`dbt/include/databricks/macros/relations/view/alter.sql`) handles `tags`, `tblproperties`, `query`, and `column_comments` from the configuration changeset but has no branch for `column_tags` — while `ViewConfig.config_components` includes `ColumnTagsProcessor` and a column-tags-only change does not set `requires_full_refresh` (so it routes to `alter_view` rather than a full replace). When column tags are the only change, the macro becomes a no-op that never calls `statement('main')`, which dbt treats as an error.

### Scope

Only affects views with `view_update_via_alter: true` (non-default) that use column tags. The create path and the `table` / V2-incremental paths are unaffected. The analogous V1-incremental column-tags drop is tracked in #1307 (fixed in #1520).

### System information

- **dbt-databricks**: main
- **Platform**: Unity Catalog

