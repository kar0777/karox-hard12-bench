You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

dbt Classes Instance Methods is_string, is_numeric, is_number, is_float don't seem to work

### Describe the bug
The same issue with the methods persists in the Databricks adapter as was reported in the Spark adapter in [this issue](https://github.com/dbt-labs/dbt-spark/issues/658).

dbt Classes Instance Methods is_string, is_numeric, is_number, is_float don't seem to work

For our instance, `col.is_string()` does not works, and for one of our customers, the `col.is_number()` also does not work.

### Steps To Reproduce
- Take any string field output from `get_columns_in_relation` and print the result of `col.is_string()`.

### Expected behavior

- When `col.datatype == 'string'` then `col.is_string()` should evaluate to true.

### Screenshots and log output

- I ran this print statement.

```
{{ print('Column: ' ~ col.name ~ ' | Data Type: ' ~ col.data_type ~ ' | Is Number: ' ~ col.is_number() ~ ' | Is String: ' ~ col.is_string()) }}
```

And the result shows it's not identifying correctly.
```
Column: name03 | Data Type: string | Is Number: False | Is String: False
```


### System information
**The output of `dbt --version`:**
```
Core:
  - installed: 1.11.6
  - latest:    1.11.7 - Update available!

Plugins:
  - databricks: 1.11.6 - Up to date!
```

**The operating system you're using:** 
macOS

**The output of `python --version`:** 
Python 3.13.9

### Additional context
Add any other context about the problem here.

