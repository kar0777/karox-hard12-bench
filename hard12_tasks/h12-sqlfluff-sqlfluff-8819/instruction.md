You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

CV06 multiline_newline fix comments out the following statement

### Search before asking

This is the separate newline-path follow-up to #8810, coordinated in https://github.com/sqlfluff/sqlfluff/issues/8810#issuecomment-6314588593. #8811 intentionally handles only `_handle_semicolon_same_line()`; this issue is not a regression attributed to that PR.

### What Happened

With `multiline_newline = True`, moving a multiline statement's semicolon ahead of a standalone line comment can delete the newline that terminates that comment. The following statement becomes comment text.

### Expected Behaviour

Formatting must preserve both statements and their execution results.

### Observed Behaviour

Input:

```sql
SELECT
1
-- c
;SELECT 2;
```

CV06 output:

```sql
SELECT
1
;
-- cSELECT 2;
```

The output still parses, passes CV06, and is unchanged by another fix. An equivalent synthetic INSERT example leaves only the first of two rows in a fresh in-memory SQLite database. A DELETE example also changes the final row set.

### How to reproduce

Save the input as `example.sql` and the configuration below as `.sqlfluff`, then run:

```sh
sqlfluff fix --rules CV06 example.sql
sqlfluff lint --rules CV06 example.sql
```

### Dialect

Reproduced with SQLFluff's ANSI and SQLite dialect configurations. Execution checks use SQLite only.

### Version

SQLFluff 4.4.0, Python 3.12. Also reproduced from current main `ad1231eab8ad9951e186f3a695e8e9abc586300d` with the Python parser and raw templater. The existing 62 CV06 YAML cases pass on that main baseline. This is not an execution test of #8811's head.

### Configuration

```ini
[sqlfluff]
dialect = sqlite
templater = raw
rules = CV06
processes = 1
use_rust_parser = False

[sqlfluff:rules:convention.terminator]
multiline_newline = True
```

### Are you willing to work on and submit a PR to address the issue?

Yes. I am preparing a narrowly scoped newline-path fix and regression tests, leaving the same-line and nested-statement work to their existing PRs.

### Code of Conduct

I will follow the project's Code of Conduct.

### Validation disclosure

Investigation and this report are AI-assisted. Synthetic execution checks and a separately written probe verified the statement/result loss; no real data or production systems were used.
