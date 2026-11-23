You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Renaming a struct that holds identifier fields fails with "Cannot find identifier field"

### Apache Iceberg version

main (development)

### Please describe the bug

Renaming a struct column that contains an identifier field fails at commit:

```python
schema = Schema(
    NestedField(1, "user", StructType(NestedField(2, "id", LongType(), required=True)), required=True),
    identifier_field_ids=[2],
)
tbl = catalog.create_table("db.t", schema=schema)
with tbl.update_schema() as update:
    update.rename_column("user", "account")
# ValueError: Cannot find identifier field user.id. In case of deletion, update the identifier fields first.
```

The rename keeps every field ID, and the spec stores identifier fields by ID, so the identifier should follow the rename. `UpdateSchema` keeps the identifier fields as dotted names while the update is staged, and `rename_column` only updates a name that equals the renamed column itself, so a renamed parent struct leaves `user.id` behind. Java's `SchemaUpdate.renameColumn` has the same exact-name check.

I tried a few fixes and would like a direction before opening a PR, because the names-while-staging design makes each one trade something:

1. Rewrite the names nested under the renamed column in `rename_column`. Small, but staged names can collide, for example when two structs swap names, or when a case-insensitive update meets columns that differ only in case. Some of these updates work today.
2. Keep identifier fields by field ID while staging. Renames then just work, but `set_identifier_fields` needs a rule for which schema its names refer to (the starting schema like the other `UpdateSchema` methods, or the final one like Java), and either rule changes the result of some updates that work today.
3. Keep today's name lookup, and fall back to field IDs recorded at rename time only when a name no longer resolves. Updates that work today give the same result, but the fallback needs care so that it never picks a different field, which takes a few dozen lines.

Would you prefer 2, or 3 to stay compatible?

### Willingness to contribute

- [x] I can contribute a fix for this bug independently

This issue was written by Isaac.

