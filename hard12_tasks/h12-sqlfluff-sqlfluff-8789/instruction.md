You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

using return() values in nested macros from the same file result in rendering only inner result

### Search before asking

- [x] I searched the [issues](https://github.com/sqlfluff/sqlfluff/issues) and found no similar issues.


### What Happened

We have a dbt project where we define a "local variable" by putting it in a macro with a return statement and using that in macros, everything in the same file since it is impossible to define variables outside of certain jinja blocks and the global variable/dbt_project.yaml.

When using the nested macro in our SQL codebase, `sqlfluff lint` produces 'PRS' errors, due to malformed SQL. It produces invalid results by only outputting the return value of the inner macro and dropping any rendering from the outer one.

This only happens on nested macros when using `return()` in the inner macro and having the inner and outer macro in the same file.

We have this for convenience: Having a _local variable_ section at the top of the file where it is easy to change and one or two macros with a similar scope below using that variable

### Expected Behaviour

Same as when using nested macro calls separated into multiple files.

### Observed Behaviour

see below and above

### How to reproduce

macros/multi.sql
```jinja
{%- macro nested_broken() -%}
  {%-do return({
    "a": "x",
    "b": "y",
  }) -%}
{%- endmacro -%}

{%- macro outer_broken(in_col, out_col) %}
  {%- set nested_value = nested_broken() %}
  CASE {{ in_col }}
  {%- for when, then in nested_value.items() %}
    WHEN {{ when }} THEN {{ then }}
  {%- endfor %}
  END AS {{ out_col }}
{%- endmacro %}

{%- macro outer_working(in_col, out_col) %}
  {%- set nested_value = nested_working() %}
  CASE {{ in_col }}
  {%- for when, then in nested_value.items() %}
    WHEN {{ when }} THEN {{ then }}
  {%- endfor %}
  END AS {{ out_col }}
{%- endmacro %}
```

macros/single.sql
```jinja
{%- macro nested_working() %}
  {%-do return({
    "a": "x",
    "b": "y",
  }) %}
{%- endmacro %}
```

models/example.sql
```jinja
SELECT
    {{ outer_broken("in", "out") }}
FROM my_table;
-------
SELECT
    {{ outer_working("in", "out") }}
FROM my_table;
```

execute:
```bash
sqlfluff render models/example.sql
```

output:
```sql
SELECT
    {'a': 'x', 'b': 'y'}
FROM my_table;
-------
SELECT
    
  CASE in
    WHEN a THEN x
    WHEN b THEN y
  END AS out
FROM my_table;
```

### Dialect

bigquery, ansi

### Version

4.3.0, 4.4.0

### Configuration

[sqlfluff]
dialect = bigquery
templater = jinja

[sqlfluff:templater:jinja]
apply_dbt_builtins = True
load_macros_from_path = macros

### Are you willing to work on and submit a PR to address the issue?

- [ ] Yes I am willing to submit a PR!

### Code of Conduct

- [x] I agree to follow this project's [Code of Conduct](https://github.com/sqlfluff/sqlfluff/blob/main/CODE_OF_CONDUCT.md)

