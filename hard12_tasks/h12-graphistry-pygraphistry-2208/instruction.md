You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

GFQL Cypher: ORDER BY a backtick alias containing a space fails order_by validation

## Summary

0.61.0 added backtick identifiers in Cypher (#2198). An alias that contains a space works in `RETURN`, but `ORDER BY` on that alias fails validation:

```
GFQLTypeError [type-mismatch] Invalid type for parameter 'keys' in 'order_by' | field: params.keys | value: "list: [('the id', 'desc')]"
```

## Repro

```python
import pandas as pd, graphistry
n = pd.DataFrame({'id': ['a', 'b', 'c'], 'score': [3, 1, 2]})
g = graphistry.nodes(n, 'id').edges(pd.DataFrame({'s': ['a'], 'd': ['b']}), 's', 'd')

g.gfql("MATCH (n) RETURN n.id AS `the id` ORDER BY `the id` DESC")   # error
```

| Query | 0.61.0 and master (0b6f88d8) |
|---|---|
| ``RETURN n.id AS `theid` ORDER BY `theid` DESC`` | OK |
| ``RETURN n.id AS `the id` `` (no ORDER BY) | OK |
| `RETURN n.id AS i ORDER BY i DESC` | OK |
| ``RETURN n.id AS `the id` ORDER BY `the id` DESC`` | **type-mismatch error** |

On 0.60.0 all of the backtick forms are syntax errors, so this is a gap in the new feature, not a regression. The `order_by` key validation seems to reject a column name that contains a space.

