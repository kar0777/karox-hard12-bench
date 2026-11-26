You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

When parsing a segment of SQL, although the field-level relationships exist, the source table information is lost.

**Describe the bug**
When parsing a segment of SQL, although the field-level relationships exist, the source table information is lost.
 existing table prefixes have also been replaced with "default.".

**SQL**
Paste the SQL text here. For example:
```sql=
insert into foo.tb1  select f1,f2,(select f3 from  bar.tb1) b3 from  foo.tb2
```


For example:
```pycharm  run 

MetaData = {"bar.tb1": ["f1", "f2", "f3"]}

provider = DummyMetaDataProvider(MetaData)

LineageRunner = sqllineage.runner.LineageRunner(sql, metadata_provider=provider, verbose=True)

LineageRunner.print_column_lineage()
print("=======source_tables:")
print(LineageRunner.source_tables)
```

result:
```
foo.tb1.b3 <- <default>.tb1.f3
foo.tb1.f1 <- foo.tb2.f1
foo.tb1.f2 <- foo.tb2.f2
=======source_tables:
[Table: foo.tb2]
```


**Expected behavior**
I hope to correctly display the prefix **bar. for  tb1.f3**    and **bar.tb1 in source_tables**

**Python version (available via `python --version`)**
 - 3.8.17


**SQLLineage version (available via `sqllineage --version`):**
 - 1.5.3

**Additional context**
Add any other context about the problem here.

