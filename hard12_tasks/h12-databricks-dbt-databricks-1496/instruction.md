You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

partition_by on managed Iceberg incremental models silently loses clustering after first incremental run

### Describe the bug

On a **managed Iceberg** (`table_format="iceberg"` with the `use_managed_iceberg` flag) **incremental** model configured with `partition_by`, the table is correctly clustered after the initial `CREATE` but loses **all** clustering after the **first incremental run**. The run succeeds with no error; the table ends up with both `clusteringColumns=[]` and `partitionColumns=[]`. Query performance then degrades silently.

This shares the `apply_liquid_clustered_cols` → `ALTER TABLE … CLUSTER BY NONE` mechanism with #805, but #805 was on **Delta** tables partitioned **outside** dbt and *errored loudly*. This case is on managed Iceberg created **inside** dbt and *fails silently*. (A maintainer comment on #805 noted the ALTER wouldn't be attempted if the partition existed inside dbt — that holds for Delta but **not** for managed Iceberg, for the reason below.)

**Root cause:** Managed Iceberg on Unity Catalog normalizes `PARTITION BY` into liquid-clustering keys server-side, so `DESCRIBE DETAIL` reports the partition columns as `clusteringColumns`. On the incremental run the reconciler compares desired vs existing clustering:

- **Desired** — `LiquidClusteringProcessor.from_relation_config` reads *only* `liquid_clustered_by`/`auto_liquid_cluster`, never `partition_by` → `cluster_by=[]`.
- **Existing** — `from_relation_results` reads the live `clusteringColumns` → `["business_date"]`.

The phantom diff puts `liquid_clustering` in the changeset, so `apply_liquid_clustered_cols` is called with an empty `cluster_by` and emits `ALTER TABLE … CLUSTER BY NONE`. Delta is unaffected because it stores partition columns as `partitionColumns` (not clustering), so no diff arises. `IncrementalTableConfig` also omits `PartitionedByProcessor` entirely, unlike `StreamingTableConfig`.

### Steps To Reproduce

Managed Iceberg incremental model with `partition_by`:

```sql
-- models/iceberg_partition_inc.sql
{{ config(
    materialized = "incremental",
    table_format = "iceberg",
    incremental_strategy = "merge",
    unique_key = "id",
    partition_by = ["business_date"],
) }}
select 1 as id, 'initial' as status, cast('2024-01-01' as date) as business_date
```

```yaml
# dbt_project.yml
flags:
  use_managed_iceberg: true
```

1. `dbt run` → `DESCRIBE DETAIL` shows `clusteringColumns = [business_date]`. ✅
2. Change the model to emit more than one row (trigger an incremental MERGE), then `dbt run` again.
3. `DESCRIBE DETAIL` now shows `clusteringColumns = []` and `partitionColumns = []`. ❌ `DESCRIBE HISTORY` shows an `ALTER … CLUSTER BY NONE` after the MERGE.

```
v3 | CLUSTER BY                        | clusterBy=-                  partitionBy=-
v2 | SET TBLPROPERTIES                 | clusterBy=-                  partitionBy=-
v1 | MERGE                             | clusterBy=["BusinessDate"]   partitionBy=-
v0 | CREATE OR REPLACE TABLE AS SELECT | clusterBy=["BusinessDate"]   partitionBy=[]
```

### Expected behavior

Clustering derived from `partition_by` on a managed Iceberg table should survive incremental runs. dbt should not issue `CLUSTER BY NONE` when the only reason the desired clustering looks empty is that the model uses `partition_by` (which managed Iceberg stores as clustering) rather than `liquid_clustered_by`.

### Workaround

Use `liquid_clustered_by` instead of `partition_by` in the model config. This is verified working and aligns with Databricks' recommendation for new managed-Iceberg tables.

### System information

**The output of `dbt --version`:**
```
dbt-core 1.11.x
dbt-databricks 1.12.x
```
(reproduced functionally on a UC SQL warehouse; the originating customer's exact DBR/connector versions are TBD)

### Additional context

Related: #805, #826. Reproduced with a functional test extending `TestIcebergIncrementalMerge` (managed Iceberg + `partition_by`): asserts `CLUSTER BY NONE` is emitted post-merge and that `DESCRIBE DETAIL` clustering is empty afterward.

