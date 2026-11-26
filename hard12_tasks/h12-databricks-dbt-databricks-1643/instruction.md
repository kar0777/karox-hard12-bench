You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Excessive information_schema queries from constraint-existence checks on models with primary_key set but contract not enforced

### Describe the bug

For models that declare a model-level `primary_key` property but do **not** have `contract.enforced: true` and do **not** have an explicit `constraints:` block, dbt-databricks still runs a full "does this constraint already exist?" lookup against `information_schema` on every run, for every such model.

This generates 2 queries per model with a `primary_key` set (against `information_schema.key_column_usage` and `information_schema.table_constraints`), plus an additional query against `information_schema.referential_constraints` for any foreign keys. No constraint is actually being applied or enforced for these models — the checks appear to run purely because the property is set.

In one project we investigated: 255 of 303 models (84%) have `primary_key` set, with `contract.enforced: false` and no `constraints` block anywhere in the project, yet every run issues the constraint-existence check for all 255 of them. In a warehouse shared across many projects, this pattern (where present) contributes disproportionately to `information_schema` query volume — enough, in our case, to help trip Unity Catalog's per-metastore rate limit (`RESOURCE_EXHAUSTED.UC_INFORMATION_SCHEMA_PER_METASTORE_DB_RATE_LIMIT_EXCEEDED`) and fail otherwise-unrelated jobs sharing that metastore. (We checked a second project in the same account with no `primary_key` usage at all, confirming this is tied to modeling convention/project, not something universal — but it's still a real cost wherever the convention is used.)

### Steps To Reproduce

1. Create a model with a model-level `primary_key` property set, but do not enable `contract.enforced` and do not define an explicit `constraints:` block, e.g.:
```yaml
models:
  - name: my_model
    primary_key: [id]
    columns:
      - name: id
```
2. Run `dbt build` (or `dbt run`) with debug logging (`--debug`) against a Databricks/Unity Catalog target.
3. Observe in the debug log that dbt-databricks issues a query similar to:
```sql
SELECT kcu.constraint_name, kcu.column_name
FROM `<catalog>`.information_schema.key_column_usage kcu
WHERE kcu.table_catalog = '...'
  AND kcu.table_schema = '...'
  AND kcu.table_name = 'my_model'
  AND kcu.constraint_name = (
    SELECT constraint_name
    FROM `<catalog>`.information_schema.table_constraints
    WHERE table_catalog = '...'
      AND table_schema = '...'
      AND table_name = 'my_model'
      AND constraint_type = 'PRIMARY KEY'
  )
ORDER BY kcu.ordinal_position;
```
4. Repeat for every model with `primary_key` set — query count scales linearly with the number of such models, regardless of whether any constraint is actually meant to be applied.

### Expected behavior

Constraint-existence checks (and any subsequent DDL) should only run for models where a constraint is actually going to be applied/enforced — i.e., where `contract.enforced: true` and/or an explicit `constraints:` block is present. A model-level `primary_key` property used purely for documentation/lineage purposes should not trigger live `information_schema` verification queries against the warehouse on every run.

This looks related to #1342, which described constraints being applied without an enforced contract as a regression and was closed as fixed — but the behavior described here reproduces on `dbt-databricks==1.12.1`, suggesting either the fix didn't cover the `primary_key`-property-only case (no `constraints:` block at all), or this is a related but distinct code path.

Separately, #845 requests batching per-column constraint/comment operations into fewer queries — applying that kind of batching to the constraint-existence check described here would also directly mitigate the volume problem even if the "don't check at all when not enforced" fix isn't feasible short-term.

### System information

**The output of `dbt --version`:**
```
Plugins:
  - databricks: 1.12.1
```

Environment: dbt Cloud, Databricks/Unity Catalog target, multi-project account.

### Additional context

Observed via Databricks warehouse-side error `RESOURCE_EXHAUSTED.UC_INFORMATION_SCHEMA_PER_METASTORE_DB_RATE_LIMIT_EXCEEDED`, which surfaced the underlying query volume. Table/schema/catalog identifiers have been genericized here to avoid sharing customer-identifying information.
