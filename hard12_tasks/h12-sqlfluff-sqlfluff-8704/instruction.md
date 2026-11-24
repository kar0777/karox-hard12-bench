You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Dbt custom materialization macro raise error with jinja templater and is skipped with dbt templater

### Search before asking

- [X] I searched the [issues](https://github.com/sqlfluff/sqlfluff/issues) and found no similar issues.


### What Happened

When I try to lint a macro file that contains custom materialization it throws an error. 
If I use Jinja templater as for other macros - I get this
```
L:   1 | P:   0 |  TMP | Failed to parse Jinja syntax. Correct the syntax or
                       | select an alternative templater. Error: Encountered
                       | unknown tag 'materialization'.
```

If I use dbt templater, I get this - Skipped file_name because it is a macro.


### Expected Behaviour

I want to be able to lint it using jinja templater  same as others macros. 

### Observed Behaviour

I provided info in what happened.

### How to reproduce

Try to lint macro with materialize tag and not macro tag.

### Dialect

snowflake

### Version

sqlfluff, version 3.1.1

### Configuration
```ini
[sqlfluff]
dialect = snowflake
templater = dbt (tried with jinja too)
sql_file_exts = .sql
exclude_rules = layout.long_lines, ambiguous.column_count, structure.column_order, references.keywords, references.special_chars
processes = 2
runaway_limit = 10
max_line_length = 160
indent_unit = space
large_file_skip_byte_limit = 0

[sqlfluff:indentation]
tab_space_size = 4
indented_using_on = True
indented_on_contents = False
indented_then = True
allow_implicit_indents = True

[sqlfluff:layout:type:comma]
spacing_before = touch
line_position = leading
spacing_after = single

[sqlfluff:structure.simple_case]
[sqlfluff:structure.else_null]

[sqlfluff:layout.indent]

[sqlfluff:layout.functions]

[sqlfluff:rules:convention.coalesce]

[sqlfluff:rules:convention.not_equal]
preferred_not_equal_style = c_style

[sqlfluff:rules:convention.casting_style]
preferred_type_casting_style = shorthand

[sqlfluff:rules:convention.terminator]
multiline_newline = True

[sqlfluff:rules:references.special_chars]
additional_allowed_characters = '" '

[sqlfluff:rules:ambiguous.column_references]
group_by_and_order_by_style = explicit


### aliasing rules
[sqlfluff:rules:aliasing.table]
aliasing = explicit

[sqlfluff:rules:aliasing.column]
aliasing = explicit

[sqlfluff:rules:aliasing.expression]
allow_scalar = True


### capitalisation rules
[sqlfluff:rules:capitalisation.keywords] 
capitalisation_policy = lower

[sqlfluff:rules:capitalisation.types]
extended_capitalisation_policy = lower

[sqlfluff:rules:capitalisation.identifiers]
extended_capitalisation_policy = lower

[sqlfluff:rules:capitalisation.functions]
extended_capitalisation_policy = lower

[sqlfluff:rules:capitalisation.literals]
capitalisation_policy = lower
```

### Are you willing to work on and submit a PR to address the issue?

- [ ] Yes I am willing to submit a PR!

### Code of Conduct

- [X] I agree to follow this project's [Code of Conduct](https://github.com/sqlfluff/sqlfluff/blob/main/CODE_OF_CONDUCT.md)

