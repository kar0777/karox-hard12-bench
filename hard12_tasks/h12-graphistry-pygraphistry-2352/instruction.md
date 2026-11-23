You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

GFQL Cypher: WITH ... WHERE rewrite ignores quantifier scope (any(n IN ... WHERE n.prop ...) drops rows)

## Summary

A quantifier inside a `WITH ... WHERE` filter does not respect scope. If its loop variable reuses the name of a matched alias, the predicate reads the outer alias, and rows are silently dropped.

## Repro (master `73a9ecbf1`, pandas and cuDF; verified on the DGX)

```cypher
MATCH (n) WITH n.tags AS t WHERE any(n IN [{tags:'z'}] WHERE n.tags = 'z') RETURN t
-- 2-node graph; actual: [] ; expected: 2 rows (the quantifier is always true)
```

Polars declines with its row-op `NotImplementedError` (where_rows).

## Likely cause

The `WITH ... WHERE` rewrite (`lowering.py` ~1284) substitutes or projects alias references without regard to comprehension/quantifier scope. Draft PR #2328 fixes the row-expression evaluator's scoping (#2325/#2331), but this lowering-time rewrite path is separate.

## Expected

Locals shadow outer aliases inside their scope in every clause position, including the `WITH ... WHERE` rewrite.

## Notes

- Silent wrong result (rows dropped). Found in the #2328 wave-4 review.
- It will get its own side PR off master.

