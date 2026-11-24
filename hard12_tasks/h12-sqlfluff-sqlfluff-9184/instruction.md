You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

ST01 silently deletes a comment inside a redundant ELSE NULL clause on autofix

## Summary

`ST01` (`structure.else_null`) removes a redundant `ELSE NULL` clause from a `CASE` expression when autofixing. If that `ELSE NULL` clause contains a comment (e.g. `else /* keep default */ null`), the comment is a child of the deleted `else_clause` segment, so `sqlfluff fix` silently deletes the comment along with the clause — with no warning, and no way for the user to recover it afterwards.

**Impact: data-loss**

Entry point / who reaches it: any user running `sqlfluff fix` (or `lint --fix`) with `ST01`/`structure.else_null` enabled — it's in the default `all` rule group — on a `CASE` expression whose redundant `ELSE NULL` branch carries a comment.

Reproduction:
```sql
select
    case
        when name = 'cat' then 'meow'
        when name = 'dog' then 'woof'
        else /* keep default */ null
    end
from x
```
Before this fix, `sqlfluff fix --dialect ansi --rules ST01` on the above silently drops `else /* keep default */ null` entirely, including the comment — the user's annotation is gone with no diagnostic. There is no `--fix` output, log line, or lint message that mentions the comment at all.

## Root cause

`Rule_ST01._eval` (`src/sqlfluff/rules/structure/ST01.py`), on detecting a redundant `else null`, unconditionally emits `LintFix.delete(else_clause[0])` plus deletes of the leading whitespace — deleting the entire `else_clause` segment as one unit. A comment nested between the `ELSE` keyword and the `NULL` literal is a genuine child of that segment (not a sibling the rule already preserves), so it is deleted along with the redundant clause. Nothing in the rule inspects the clause's children for a comment before deleting it.

## Fix

Before deleting the clause, look for comment children of `else_clause`. If any are found, re-home them onto their own line immediately after the last `WHEN` clause (so they attach to the `CASE` expression the same way a comment placed there manually would), then delete the clause as before. Verified this can't leave an `else_clause` with no expression child for a case ST02 might also touch, since the whole clause is still deleted as a single unit either way — only the comment is relocated, not exempted from the clause deletion.

## Testing (negative control — reproduce by execution)

Added `redundant_else_null_preserves_comment` to `test/fixtures/rules/std_rule_cases/ST01.yml`.

With the production fix reverted (fixture kept), running the targeted test fails exactly this new case and nothing else:
```
$ pytest test/rules/yaml_test_cases_test.py -k ST01 -q
FAILED test/rules/yaml_test_cases_test.py::test__rule_test_case[ST01_redundant_else_null_preserves_comment]
1 failed, 5 passed, 2501 deselected in 3.15s
```
With the fix restored:
```
$ pytest test/rules/yaml_test_cases_test.py -k ST01 -q
......                                                                   [100%]
6 passed, 2501 deselected in 2.78s
```
The new case fails without the fix and passes with it; the other 5 pre-existing ST01 cases are unaffected in both directions. Also ran `ruff check`, `ruff format --check`, `yamllint -c .yamllint`, and `mypy -p sqlfluff.rules.structure.ST01` — all clean.

## AI assistance disclosure

This change was AI-assisted: an AI agent located the bug by reading `ST01.py` and its fixtures, proposed the initial diagnosis, and drafted the fix and regression test. I manually validated it before submitting: I independently re-read `Rule_ST01._eval`'s delete-the-whole-clause logic myself rather than trusting the diagnosis as given; I ran the reproduction SQL through `sqlfluff fix` myself and read the actual (comment-dropping) output; and I ran the full test suite (negative control, full ST0* family, ruff/yamllint/mypy) myself and read the results shown above rather than taking a report of them at face value.

Signed-off-by: Udaya Tejas <udayatejas2004@gmail.com>

