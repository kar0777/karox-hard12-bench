You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

GFQL fallback drops nullable 64-bit ID matches with pandas 3.1 / NumPy 2.5

## Bug

The GFQL fallback path silently drops valid rows when the graph uses nullable 64-bit integer node identifiers with the current pandas/NumPy release pair. The indexed/fast path returns the expected row. This blocks [tck-gfql #212](https://github.com/graphistry/tck-gfql/pull/212)'s hosted CI before its new scenarios execute, but reproduces on unchanged TCK main; #212 did not introduce it.

## Source-proven reproduction

- Product: pygraphistry master `a649e05f20a2457a024722b78b6f99d3ab0aeb46`.
- TCK: main `e5bd3a2a45729c8957fc1fa71ddd22121bbc82e1`, existing `tests/cypher_tck/test_nullable_identifier_identity.py`.
- Hosted-like local env: Python 3.12.10, NumPy 2.5.4, pandas 3.1.0, pytest 9.1.1, editable exact product source. Hosted [CI run 40902482631](https://github.com/graphistry/tck-gfql/actions/runs/40902482631) used Python 3.12.15 with the same package versions and failed the same case.
- Command from TCK main: `/tmp/tck-2253-hosted-uv-env/bin/python -m pytest -q tests/cypher_tck/test_nullable_identifier_identity.py -k pandas --tb=no`. The test builds nullable `Int64`/`UInt64` node and edge IDs (including nulls), creates node/edge indexes, then queries `n(id=big+offset) -> e_forward() -> n() -> rows(source="b")` with all registered routes on or off.

| Environment | Routes on | Routes off, valid seeds 0/1 | Routes off, empty seed 2 |
|---|---:|---:|---:|
| NumPy 2.2.6 / pandas 2.3.3 | 6/6 pass | 4/4 pass | 2/2 pass |
| NumPy 2.5.4 / pandas 3.1.0 | 6/6 pass | **4/4 fail** | 2/2 pass |

For both `Int64` near 2^53 and `UInt64` near 2^63, the failing fallback cases expect one matched destination but return zero rows. Running just the first failing test against both TCK main and #212 produces the same result. The package-pair boundary is proven; pandas versus NumPy as the individual cause is not yet isolated.

## Acceptance

- Find and fix the generalized nullable/exact-integer ID loss in the fallback path; preserve identity and row counts across route-on/off, null placements, Int64/UInt64, and values beyond float exactness. Avoid a special case keyed to this test.
- Add positive valid-seed, partial/null, and empty negative oracles on both sides of the changed boundary. Validate pandas under both package pairs; check Polars, Polars-GPU, and cuDF where the changed code path applies, or record a precise nonapplicability/typed decline.
- Preserve static typing and existing index semantics. If a hot path or index route changes, add a source-pinned pyg-bench parity/performance control before claiming no regression.
- Require focused tests, exact-head hosted CI/TCK, and DGX GPU validation where applicable before landing. Coordinate with #2253/#212; do not mask the failure by pinning TCK CI to older pandas without a separate support-floor decision.

Related but distinct: #1890 tracks other pandas-3 latents and CI gaps; closed #2058 tracked route-dependent integer dtype upcasting.

