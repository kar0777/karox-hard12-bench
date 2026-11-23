You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

GFQL Cypher: keys(n) in multi-alias queries returns internal binding columns (size 6 instead of 2)

## Summary

`keys(n)` returns internal binding column names in any query that matches more than one alias. This happens on master even outside comprehensions.

## Repro (master `73a9ecbf1`, pandas, 2-node graph with columns `id` and `tags`; verified on the DGX)

```cypher
MATCH (n),(m) RETURN keys(n) AS k
-- actual:   ['id_x', 'n.id', 'n.tags', 'id_y', 'm.id', 'm.tags']
-- expected: ['id', 'tags']

MATCH (n),(m) RETURN size(keys(n)) AS s
-- actual: 6
-- expected: 2
```

## Likely cause

In multi-alias row frames, `keys(n)` enumerates the joined row's columns, including merge suffixes and other aliases' prefixed columns. It should enumerate only `n`'s entity properties.

## Expected

`keys(n)` returns exactly `n`'s property keys (non-null, per openCypher), independent of how many aliases are matched. The same applies to `properties(n)`, and to `keys(r)` for relationships.

## Notes

- Silent wrong result. Found while reviewing #2328; it is not part of #2328's scope.
- Suggested acceptance: tests on pandas, cuDF and Polars for `keys(n)` / `properties(n)` with 2+ aliases, including same-named properties on different aliases.

