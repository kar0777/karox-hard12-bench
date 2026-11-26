You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Getting column lineage from subquery with column name specified

**Describe the bug**
Relations are wrong when using intermediate tables on column level. When using a intermediate table and naming its columns, it is describing the columns as the Table/Subquery instead of the table name specified.

**SQL**

```sql
insert into db_test.table_target
select col_1_renamed, col_2_renamed from
(Select col1, max(col2) from db_test.table_src
where
  col1 = "AV" and
  col2 is not null
) AS Inter_table(col_1_renamed, col_2_renamed);
```

**To Reproduce**

```python
from sqllineage.runner import LineageRunner, LineageLevel

query = """ insert into db_test.table_target
select col_1_renamed, col_2_renamed from
(Select col1, max(col2) from db_test.table_src
where
  col1 = "AV" and
  col2 is not null
) AS Inter_table(col_1_renamed, col_2_renamed);
"""
result = (
    LineageRunner(query, dialect="teradata")
)
lineage_stmt = result.to_cytoscape(LineageLevel.COLUMN)
print(lineage_stmt)
```
```
{'data': {'id': 'db_test.table_src.col1', 'parent': 'db_test.table_src', 'parent_candidates': [{'name': 'db_test.table_src', 'type': 'Table'}], 'type': 'Column'}}
{'data': {'id': '(col_1_renamed, col_2_renamed).col1', 'parent': '(col_1_renamed, col_2_renamed)', 'parent_candidates': [{'name': '(col_1_renamed, col_2_renamed)', 'type': 'SubQuery'}], 'type': 'Column'}}
{'data': {'id': 'db_test.table_src.col2', 'parent': 'db_test.table_src', 'parent_candidates': [{'name': 'db_test.table_src', 'type': 'Table'}], 'type': 'Column'}}
{'data': {'id': '(col_1_renamed, col_2_renamed).max(col2)', 'parent': '(col_1_renamed, col_2_renamed)', 'parent_candidates': [{'name': '(col_1_renamed, col_2_renamed)', 'type': 'SubQuery'}], 'type': 'Column'}}
{'data': {'id': '(col_1_renamed, col_2_renamed).col_1_renamed', 'parent': '(col_1_renamed, col_2_renamed)', 'parent_candidates': [{'name': '(col_1_renamed, col_2_renamed)', 'type': 'SubQuery'}], 'type': 'Column'}}
{'data': {'id': 'db_test.table_target.col_1_renamed', 'parent': 'db_test.table_target', 'parent_candidates': [{'name': 'db_test.table_target', 'type': 'Table'}], 'type': 'Column'}}
{'data': {'id': '(col_1_renamed, col_2_renamed).col_2_renamed', 'parent': '(col_1_renamed, col_2_renamed)', 'parent_candidates': [{'name': '(col_1_renamed, col_2_renamed)', 'type': 'SubQuery'}], 'type': 'Column'}}
{'data': {'id': 'db_test.table_target.col_2_renamed', 'parent': 'db_test.table_target', 'parent_candidates': [{'name': 'db_test.table_target', 'type': 'Table'}], 'type': 'Column'}}
{'data': {'id': 'db_test.table_src', 'type': 'Table'}}
{'data': {'id': '(col_1_renamed, col_2_renamed)', 'type': 'SubQuery'}}
{'data': {'id': 'db_test.table_target', 'type': 'Table'}}
{'data': {'id': 'e0', 'source': 'db_test.table_src.col1', 'target': '(col_1_renamed, col_2_renamed).col1'}}
{'data': {'id': 'e1', 'source': 'db_test.table_src.col2', 'target': '(col_1_renamed, col_2_renamed).max(col2)'}}
{'data': {'id': 'e2', 'source': '(col_1_renamed, col_2_renamed).col_1_renamed', 'target': 'db_test.table_target.col_1_renamed'}}
{'data': {'id': 'e3', 'source': '(col_1_renamed, col_2_renamed).col_2_renamed', 'target': 'db_test.table_target.col_2_renamed'}}
```

**Expected behavior**
The code should detect Inter_table as the Subquery and not (col_1_renamed, col_2_renamed) as a whole. The column lineage as source and target should be:
db_test.table_src.col1 -> Inter_table.col_1_renamed
db_test.table_src.col2 -> Inter_table.col_2_renamed

Inter_table.col_1_renamed -> db_test.table_target.col_1_renamed
Inter_table.col_2_renamed -> db_test.table_target.col_2_renamed


**Python version 
 - 3.10.12
 
**SQLLineage version (available via `sqllineage --version`):**
 - 1.5.3
 
**Additional context**
Looks like there is a problem when detecting intermediate tables 

