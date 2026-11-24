You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

GFQL Cypher: aggregates over a string subscript (count(a['name']), collect(...)) silently return empty results

## Problem

An aggregate over a string-subscript property read returns a wrong result without raising, while the dotted spelling of the same property is correct. `a['name']` and `a.name` should be equivalent.

## Example

Observed on `develop` at 92f28470c with the pandas engine, on a small graph where the dotted forms return the values shown:

| Query | Subscript result | Dotted result |
|---|---|---|
| `MATCH (a)-[r]->(b) RETURN count(a['name'])` | `0` | `2` |
| `MATCH (a)-[r]->(b) RETURN collect(a['name'])` | `[]` | `['x', 'y']` |
| `MATCH (a)-[r]->(b) RETURN count(r['kind'])` | `0` | `2` |
| `MATCH (a), (b) RETURN count(a['name'])` | `0` | `9` |

`count(DISTINCT b['name'])` is correct.

## Notes

- This is separate from #2336 / #2351: the binding-row subscript helper added there is not reached on the aggregate path, so the result is wrong with or without that change.
- Silent wrong answer: nothing raises or warns.

## Suggested fix

Route the aggregate argument through the same subscript-to-property resolution used for non-aggregate projections, or decline with an explicit error until supported. Add parity tests (`count`, `collect`, `min`/`max`, `sum`, with and without `DISTINCT`) across pandas, cuDF, Polars and polars-gpu, each asserting equality with the dotted spelling.

