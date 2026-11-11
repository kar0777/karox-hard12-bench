You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

cuGraph graph-return fails when user edge columns are src/dst

### Summary
`compute_cugraph(..., output="graph")` can fail when user edge columns use the temporary endpoint names `src`/`dst`. During graph-return processing, the full edge frame is renamed to literal `src`/`dst`, producing duplicate cuDF columns.

### Evidence
Observed on cuGraph `26.02.00`, cuDF `26.02.01`, RAPIDS GPU, against master/base `d220c9cdc8cf22c9c59caf9b73c2a7ea9c1eff64`. Failures:
- `src` only: `ValueError: Duplicate column names are not allowed`
- `dst` only: same duplicate-column error
- `src` + `dst`: same duplicate-column error

Controls pass with no endpoint attributes, `source`, or `target`. The failing rename is at `graphistry/plugins/cugraph.py:364`.

### Expected
Graph-return calls should reserve temporary endpoint names against every user edge column, restore them safely across one or more calls, and preserve topology and attributes. Generated-looking user names need the same treatment.

### Scope
Fix cuGraph graph-return name reservation only. Do not change unrelated cuGraph algorithms or broad exception handling. Tests should cover baseline plus `src`, `dst`, and both; repeated graph-return calls; topology/attribute identity; direct conversion controls. Establish a red test on current master before fixing. Avoid broad `RuntimeError` skips: only known CUDA/cuGraph/cuDF prerequisites may be skipped narrowly.

Internal evidence: `plans/mcp-followups-2204-2205/planner/adapter-reuse-review/cugraph-graph-narrow.json`
