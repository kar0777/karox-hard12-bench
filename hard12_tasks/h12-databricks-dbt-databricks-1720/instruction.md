You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

views with star-select semantics and config 'view_update_via_alter' are not being updated

The current v2 view materialization combined with an enabled `view_update_via_alter` config uses a changeset to determine when to actually run the `ALTER VIEW` command versus running a no-op (the other code paths will lead to unconditional `CREATE OR REPLACE` runs). The `QueryProcessor` component and its underlying `QueryConfig` will only detect changes when the actual SQL has changed. This poses an issue for views that use star select semantics, as schema changes in the queried tables will not be picked up by the diff and leading to stale views.

### Steps To Reproduce
1. materialize the following `seed.csv`:
```csv
id,msg
1,hello
```
2. run the following view model:
```sql
{{
    config(
        materialized='view',
        view_update_via_alter=True,
    )
}}
select * from {{ ref('seed') }};
```
3. update `seed.csv` and rerun:
```csv
id,msg,extra
1,hello,ben
```
4. rerun the view model: the column `extra` will not be added.

### Expected behavior
View materialization should update the schema, even if implicit via start select semantic.

