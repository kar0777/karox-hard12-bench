You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

GEXF round-trip fails when user edge attributes are source/target

### Summary
Public GEXF export/import loses edge attribute round-trip behavior when a user edge attribute is named `source` or `target`. During import, `_apply_attvalues` overwrites the XML endpoint fields in the row. Export/import then reports missing endpoint node IDs.

### Evidence
Observed against `76786f4eb5c356ff7bf1adb82a8a194bfb7e79d6`; NetworkX controls pass. Failures:
- user `source` attr: `ValueError: Invalid GEXF: edges reference missing node ids (source_attr_0, source_attr_1)`
- user `target` attr: corresponding missing endpoint IDs
- user `source` + `target`: both overwrite

The no-attribute control passes and preserves topology and attributes.

### Expected
Preserve XML endpoint `source`/`target` separately from user edge attribute titles, or explicitly reject reserved attribute titles with a structured, actionable error if lossless wire compatibility is impossible.

### Scope
Fix only GEXF endpoint/attribute collision handling. Tests should cover source-only, target-only, both, clean controls, default/custom bindings, exported and hand-authored XML, plus positive round-trip and malformed endpoint/duplicate negatives. Establish a red test on current master before fixing.

Internal evidence: `plans/mcp-followups-2204-2205/planner/adapter-reuse-review/gexf-results.json`
