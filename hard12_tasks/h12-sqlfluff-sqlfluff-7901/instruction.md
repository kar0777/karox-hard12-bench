You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Newline before dbt config block errors out sqlfluff fix

### Search before asking

- [x] I searched the [issues](https://github.com/sqlfluff/sqlfluff/issues) and found no similar issues.


### What Happened

The `sqlfluff fix` command fails with an error, if a sql file with a dbt config block starts with a newline:

```

{{
    config(
        materialized = "ephemeral",
    )
}}

SELECT 1
```

However if the empty newline at the start of the file is not present, the command runs successfully and fixes the file correctly.

### Expected Behaviour

if the file does not have the newline at the start, it would print the following:
```
==== finding fixable violations ====
=== [dbt templater] Sorting Nodes...
WARNING:thrift.transport.sslcompat:using legacy validation callback
=== [dbt templater] Compiling dbt project...
=== [dbt templater] Project Compiled.
==== no fixable linting violations found ====
All Finished 📜 🎉!
```

### Observed Behaviour

It produces the following error, pay attention to the `WARNING`:

```
==== finding fixable violations ====
=== [dbt templater] Sorting Nodes...
WARNING:thrift.transport.sslcompat:using legacy validation callback
=== [dbt templater] Compiling dbt project...
=== [dbt templater] Project Compiled.
WARNING    Skipping edit patch on uncertain templated section [('mid_point', slice(0, 60, None))], Please report this warning on GitHub along with the query that produced it.
== [models/workflow_operational/reverse_etl/sample.sql] FAIL
L:   1 | P:   1 | LT13 | Files must not begin with newlines or whitespace.
                       | [layout.start_of_file]
== [models/workflow_operational/reverse_etl/sample.sql] FAIL
1 fixable linting violations found
```


### How to reproduce

Added a reproducible sample repo here: https://github.com/deelaka/sqlfluff-issue-template-parser

### Dialect

databricks

### Version

```
sqlfluff: 4.2.1
sqlfluff-templater-dbt: 4.2.1
dot-core: 1.11.8
Python: 3.12.12
```

### Configuration

```
[sqlfluff]
dialect = databricks
templater = dbt
max_line_length = 110
processes = 2
rules = all
exclude_rules = AL07, ST06, AL05, ST02, LT15, RF01
large_file_skip_byte_limit=0
runaway_limit = 20


[sqlfluff:indentation]
indent_unit = space
indented_using_on = True
tab_space_size = 4
trailing_comments = before


[sqlfluff:layout:type:comma]
spacing_before = touch
line_position = trailing


[sqlfluff:rules:aliasing.table]
aliasing = explicit


[sqlfluff:rules:aliasing.length]
min_alias_length = 3


[sqlfluff:rules:references.keywords]
ignore_words = id


[sqlfluff:rules:ambiguous.column_references]
group_by_and_order_by_style = explicit


[sqlfluff:rules:convention.casting_style]
preferred_type_casting_style = shorthand


[sqlfluff:rules:capitalisation.keywords]
capitalisation_policy = upper
[sqlfluff:rules:capitalisation.identifiers]
capitalisation_policy = lower
[sqlfluff:rules:capitalisation.functions]
extended_capitalisation_policy = upper
[sqlfluff:rules:capitalisation.literals]
capitalisation_policy = upper
[sqlfluff:rules:capitalisation.types]
extended_capitalisation_policy = upper

[sqlfluff:layout:type:alias_expression]
# We want non-default spacing _before_ the alias expressions.
spacing_before = align
# We want to align them within the next outer select clause.
# This means for example that alias expressions within the FROM
# or JOIN clause would _not_ be aligned with them.
align_within = select_clause
# The point at which to stop searching outward for siblings, which
# in this example would likely be the boundary of a CTE. Stopping
# when we hit brackets is usually a good rule of thumb for this
# configuration.
align_scope = bracketed
```

### Are you willing to work on and submit a PR to address the issue?

- [x] Yes I am willing to submit a PR!

### Code of Conduct

- [x] I agree to follow this project's [Code of Conduct](https://github.com/sqlfluff/sqlfluff/blob/main/CODE_OF_CONDUCT.md)

