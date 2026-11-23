You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

GFQL remote: GRAPH residual predicates are dropped from the wire payload

## Summary

`gfql_remote()` drops GRAPH-binding predicates that the Cypher compiler keeps as residual filters, such as an `OR` across two properties. Locally the binding is filtered. The remote payload sends the binding unfiltered, so a remote run can return different rows from `g.gfql()`, with no error or warning.

## Version

pygraphistry `master` @ `312b86ade87477f1cb3ab3994240f6779f26af83`

## Repro

```python
import json, pandas as pd, graphistry
from graphistry.compute.gfql.cypher.parser import parse_cypher
from graphistry.compute.gfql.cypher.lowering import compile_cypher_query
from graphistry.compute.chain_remote import _compiled_to_let_json

q = "GRAPH g = GRAPH { MATCH (n) WHERE n.x > 5 OR n.y > 5 } USE g MATCH (n) RETURN n.id"
g = (graphistry.nodes(pd.DataFrame({"id": [1, 2, 3], "x": [0, 9, 0], "y": [0, 0, 0]}), "id")
     .edges(pd.DataFrame({"s": [1, 2], "d": [2, 3]}), "s", "d"))
print(g.gfql(q)._nodes.to_dict("records"))
c = compile_cypher_query(parse_cypher(q))
print([b.graph_residual_filters for b in c.graph_bindings])
print(json.dumps(_compiled_to_let_json(c)["bindings"]["g"]))
```

Output (2026-11-07):

```
[{'n.id': 2}]
[(CompiledGraphResidualFilter(alias='n', kind='node', expr='((n.x > 5) OR (n.y > 5))', pre_filters=()),)]
{"type": "Chain", "chain": [{"type": "Node", "filter_dict": {}, "name": "n"}]}
```

With `requests.post` mocked, `g.gfql_remote(q)` POSTs the same unfiltered binding as `gfql_query.bindings.g`.

## Expected

The remote payload keeps the binding's filter, or `gfql_remote()` raises before sending when the wire format cannot express it.

## Actual

The residual filter is not serialized. The binding is sent as an unfiltered node match. Server-side results were not checked.

## Cause pointer

`graphistry/compute/chain_remote.py:78-100` (`_step_to_json`) serializes `chain.to_json()` only and ignores the compiled binding's `graph_residual_filters`.

## Suggested outcome

Serialize residual filters into the wire format, or raise `GFQLValidationError` before sending when a binding has residual filters the wire format cannot carry. A test that compares the local result with the remote payload for an `OR` binding predicate would cover it.

## Related

#1706 added the local residual GRAPH masks; #1955 is a separate remote Let/DAG gap (empty `gfql_operations`).

