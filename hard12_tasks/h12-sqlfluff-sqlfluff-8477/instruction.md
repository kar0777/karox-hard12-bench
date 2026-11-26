You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Nested Jinja context not working when defined in pyproject.toml (since 3.2.0 only)

### Search before asking

- [X] I searched the [issues](https://github.com/sqlfluff/sqlfluff/issues) and found no similar issues.


### What Happened

Nested Python dictionaries used as Jinja context variables are no longer handled correctly in `sqlfluff` 3.2.0 and up, when defined in `pyproject.toml` and not `.sqlfluff`.

### Expected Behaviour

Sample SQL:
```sql
select
    {% for metric in bundle.selected_metrics -%}
        coalesce({{ metric.definition }}, 0)::float as {{ metric.name }},
    {% endfor -%}
    '123' as bar
from data;
```

Sample pyproject.toml:

```toml 
[tool.sqlfluff.templater.jinja.context]
bundle  = {safe_name = 'test_metric', base_sql = 'select 1', join_key = 'user_id', selected_metrics = [{name = 'logged_days', definition='COUNT(*)'}]}

[tool.sqlfluff.core]
templater = "jinja"
dialect = "snowflake"
```

sample `.sqlfluff`:
```
[sqlfluff]
templater = jinja
dialect=snowflake

[sqlfluff:templater:jinja:context]
bundle = {'safe_name': 'test_metric', 'base_sql': 'select 1', 'join_key': 'user_id', 'selected_metrics' : [{'name':'logged_days', 'definition':'COUNT(*)'}]}
```

Expected behavior: linting passes successfully, such as when using `.sqlfluff`

```
uvx sqlfluff lint test.sql --config .sqlfluff --ignore-local-config --- passes
```




### Observed Behaviour

The same configuration fails when using pyproject.toml

```
uvx sqlfluff lint test.sql --config pyproject.toml --ignore-local-config
== [test.sql] FAIL
L:   2 | P:   1 | LT02 | Line should not be indented. [layout.indent]
L:   2 | P:  49 | LT02 | Expected indent of 4 spaces. [layout.indent]
L:   3 | P:  17 |  PRS | Line 2, Position 13: Found unparsable section: "(,
                       | 0)::float as ,\n    '123' as bar"
WARNING: Parsing errors found and dialect is set to 'snowflake'. Have you configured your dialect correctly?
All Finished 📜 🎉!

```

However, it works with sqlfluff 3.1.1:

```
uvx sqlfluff@3.1.1 lint test.sql --config pyproject.toml --ignore-local-config
All Finished 📜 🎉!
```



### How to reproduce

See above.

### Dialect

snowflake (likely dialect independent)

### Version

Tested with both 3.3.0 and 3.2.0/3.2.5

### Configuration

See above

### Are you willing to work on and submit a PR to address the issue?

- [X] Yes I am willing to submit a PR!

### Code of Conduct

- [X] I agree to follow this project's [Code of Conduct](https://github.com/sqlfluff/sqlfluff/blob/main/CODE_OF_CONDUCT.md)

