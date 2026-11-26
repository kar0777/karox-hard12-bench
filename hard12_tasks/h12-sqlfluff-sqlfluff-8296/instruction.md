You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

ST06: causes displacement of inline comments

### Search before asking

- [X] I searched the [issues](https://github.com/sqlfluff/sqlfluff/issues) and found no similar issues.


### What Happened

When L034 is fixed (with any dialect I have tried, including postgres, sqlite and bigquery), inline comments of rearranged lines does not follow said rearrangement. 

The following is a minimal example:

```sql
SELECT
    (a - b) AS calc_alias,  -- calc_alias comment
    a AS a_alias  -- a_alias comment
FROM
    table
```

This violates rule `L034: Select wildcards then simple targets before calculations and aggregates.`

### Expected Behaviour

After applying the fix suggested by `sqlfluff fix . --dialect postgres` (or any other dialect), I would expect the query to end up as

```sql
SELECT
    a AS a_alias,  -- a_alias comment
    (a - b) AS calc_alias  -- calc_alias comment
FROM
    table
```

### Observed Behaviour

After applying the fix suggested by `sqlfluff fix . --dialect postgres` (or any other dialect, it seems), the query ends up as

```sql
SELECT
    a AS a_alias, -- calc_alias comment
    (a - b) AS calc_alias -- a_alias comment
FROM
    table
```

where the comments can be seen to be misplaced. 

### How to reproduce

Create the query

```sql
SELECT
    (a - b) AS calc_alias,  -- calc_alias comment
    a AS a_alias  -- a_alias comment
FROM
    table
```

and run `sqlfluff fix . --dialect postgres`

### Dialect

Reproduced with all tried dialects, including postgres, sqlite, and bigquery. 

### Version

sqlfluff 1.4.1 and Python 3.9.13

### Configuration

None

### Are you willing to work on and submit a PR to address the issue?

- [ ] Yes I am willing to submit a PR!

### Code of Conduct

- [X] I agree to follow this project's [Code of Conduct](https://github.com/sqlfluff/sqlfluff/blob/main/CODE_OF_CONDUCT.md)

