You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

GFQL 0.61.2: timezone-aware datetime equality loses matches for plain date strings

### Summary

PyGraphistry 0.61.2 loses matches when a timezone-aware `datetime64` node property is compared for equality with a plain date string. The same query returns the expected row on 0.61.1. Equivalent inclusive range comparisons still return the row.

The regression affects literal Cypher, public `n(filter_dict)` ASTs, and serialized/deserialized node JSON.

### Reproduction

```python
import pandas as pd
import graphistry
from graphistry.compute.ast import n

nodes = pd.DataFrame({
    "id": ["a", "b"],
    "tsz": pd.to_datetime(["2024-01-01T00:00:00Z", "2024-01-02T00:00:00Z"]),
})
edges = pd.DataFrame({"s": ["a"], "d": ["b"]})
g = graphistry.nodes(nodes, "id").edges(edges, "s", "d")

assert g.gfql("MATCH (n) WHERE n.tsz = '2024-01-01' RETURN n.id AS id", engine="pandas")._nodes["id"].tolist() == ["a"]
```

| Entry point | 0.61.1 | 0.61.2 |
|---|---:|---:|
| Cypher equality (`n.tsz = '2024-01-01'`) | `["a"]` | `[]` |
| Inclusive range (`>=`/`<=` at the same bound) | `["a"]` | `["a"]` |
| `n(filter_dict)` AST equality | `["a"]` | `[]` |
| Serialized then deserialized JSON AST equality | `["a"]` | `[]` |

Verified with Python 3.12 and pandas 2.3.3, importing each version from separate source archives and printing `graphistry.__file__` before execution.

### Causal evidence

The 0.61.1→0.61.2 diff introduces `_coerce_temporal_filter_scalar` and invokes it before concrete property filtering (#2230). For a datetime column, a string is converted with `pd.to_datetime(value)` without considering the column timezone. A UTC-aware Series can therefore be compared with a naive parsed scalar and produce no match. Parsing the bound into a UTC/localized timestamp matches the expected row.

The plain-string datetime comparison is not a malformed-value case. It must not be fixed by globally forcing every column or literal to UTC, and non-UTC/DST/explicit-offset semantics need deliberate treatment. Malformed temporal bounds should continue to raise structured E302 errors.

### Expected behavior

Equality semantics should be stable across public Cypher, AST, and serialized-JSON entry points and must agree with equivalent inclusive range behavior for supported datetime representations.

