You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Tranche: Comparison/list/null wrong-row semantics (14 cases) under #1353

## Summary
One-PR tranche under meta-issue #1353: comparison/list/null edge semantics.

Current bucket size: 14 wrong-row cases.

## Scope (keys)
- expr-comparison1-6-5
- expr-comparison1-7-12
- expr-comparison1-7-13
- expr-comparison1-7-14
- expr-comparison1-7-15
- expr-comparison1-7-16
- expr-list5-21
- expr-list5-29
- expr-list5-31
- expr-list5-34
- expr-list12-3
- expr-list3-7
- expr-null1-3
- expr-null2-3

## Why this tranche
- Tri-valued + collection comparison semantics are common practical bug sources.
- The keys are tightly related and likely share fix loci.
- One PR scope with measurable output.

## Acceptance criteria
- Listed keys move from success_wrong_rows to success_matches_expected.
- No increase in unexpected_success_expected_error.
- Focused contract checks remain green.

## Repro
- PYTHONPATH=/home/lmeyerov/Work/pygraphistry:/home/lmeyerov/Work/tck-gfql UV_EXCLUDE_NEWER="6 days" uv run --python 3.13 --no-project --with pytest --with pandas python -m pytest -q tests/cypher_tck/test_tck_runner.py -k "test_direct_cypher_xfail_contract"

## Cross-reference
- Parent meta-issue: #1353

