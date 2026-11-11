You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

AnswerBuilder: reference_pattern is not validated and crashes run() with a cryptic int() error

## **Describe the bug**
`AnswerBuilder` validates `pattern` (at most one capture group) but never validates
`reference_pattern`. `_extract_reference_idxs` calls `int()` on whatever
`re.findall(reference_pattern, reply)` returns, so a pattern with zero capture
groups, two or more groups, or an optional group that doesn't participate crashes
`run()` with an unclear error. The crash happens only when a reply actually contains
a match, so it can pass testing and fail later on real LLM output.

**Error message**
ValueError: invalid literal for int() with base 10: '[1]'                (no group)
TypeError: int() argument must be a string, a bytes-like object or a real number, not 'tuple'   (two groups)
ValueError: invalid literal for int() with base 10: ''                  (optional group, reply "x []")

**Expected behavior**
Same behavior as `pattern`: a clear `ValueError` naming the pattern and the problem,
for example "Reference pattern '\[\d+\]' contains 0 capture groups. Please specify
a pattern with exactly one capture group that matches the document index."

**Additional context**
- `pattern` is checked via `_check_num_groups_in_regex` in `__init__` and `run`; `reference_pattern` has no equivalent check.
- `reference_pattern` is not validated in `__init__` either, and an invalid regex such as `"["` only fails at run time.
- I suggest validating the effective pattern (init value or run-time override) in `run()` only: an existing test
  (`test_run_with_reference_pattern_set_at_runtime`) constructs the component with a placeholder pattern and overrides it in `run()`.
- A prototype of this check (about 11 lines) passes the existing 33 tests in `test_answer_builder.py`.
- The default `\[(\d+)\]` pattern, including `expand_reference_ranges=True`, is not affected.
- I'm happy to open a PR for this if maintainers agree with the approach.

**To Reproduce**
from haystack import Document
from haystack.components.builders import AnswerBuilder

docs = [Document(content="a"), Document(content="b")]

*no capture group*
AnswerBuilder(reference_pattern=r"\[\d+\]").run(query="q", replies=["see [1]"], documents=docs)
- ValueError: invalid literal for int() with base 10: '[1]'

*two capture groups*
AnswerBuilder(reference_pattern=r"\[(\d+)\]\[(\d+)\]").run(query="q", replies=["x [1][2]"], documents=docs)
- TypeError: int() argument must be ... not 'tuple'

*no crash when the reply has no citation, so the problem stays hidden*
AnswerBuilder(reference_pattern=r"\[\d+\]").run(query="q", replies=["no citation"], documents=docs)

**FAQ Check**
- [x] Have you had a look at [our new FAQ page](https://docs.haystack.deepset.ai/docs/faq)?

**System:**
- OS: Linux
- Haystack version: main (3.5.0-rc0), commit 29e0fd7
