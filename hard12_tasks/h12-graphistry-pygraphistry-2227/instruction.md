You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

gfql: rows(table=nodes, source=alias) multiplies rows for duplicate node ids and joins null ids to each other

Found while pinning the seeded node-lookup fast path (parity harness on the branch for the seeded fast paths, 2026-09-04).

1. Duplicate node ids: with two node rows carrying `id = 7`, `MATCH (p {id: 7}) RETURN p.age AS a` on the full path returns 8 rows on pandas and cuDF (2 duplicate rows → 2^3 through the chain's forward/reverse/combine self-joins); polars returns 2. The expected answer is one row per matching node row (2).
2. Null ids: with two rows whose `id` is null, `MATCH (p {name: 'n3'}) RETURN p.id, p.age` returns both null-id rows on the full path (NaN-keyed merge matches NaN to NaN) instead of the one row that matches the predicate. A seeded typed hop whose seed row has a null id raises `GFQLTypeError` on the full path (merge object vs float64) instead of returning no rows.

The seeded fast paths (`_execute_seeded_node_lookup_fast_path`, `_execute_seeded_typed_hop_fast_path`) return the intended answer for these inputs; `graphistry/tests/compute/gfql/test_seeded_node_lookup_fastpath.py::test_node_lookup_returns_each_duplicate_id_row_once` pins the fast answer on all three engines. The full path should agree; until it does, the differential parity tests exclude duplicate and null ids.

Where: `graphistry/compute/chain.py` `_chain_impl` combine step (self-join on the node id) and `graphistry/compute/gfql/row/frame_ops.py` `rows(source=...)`; the merges should key on row position for node-frame lookups, and null ids must never link.
