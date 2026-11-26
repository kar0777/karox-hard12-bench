You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Support `REPLACE USING` for INSERT

**Is your feature request related to a problem? Please describe.**
I am trying to parse a Databricks SQL as such
```
import sqlglot

# https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-dml-insert-into#replace-using
sql = """
INSERT INTO TABLE students
    REPLACE USING (country)
    SELECT * FROM new_students;
"""
sqlglot.parse_one(sql, dialect="databricks"
```

But currently the core parser/generator does not handle such case, and are impossible to be overridden at dialect level.

**Describe the solution you'd like**

I would like the core parser/generator to support this `REPLACE USING` expression.

**Describe alternatives you've considered**

I think the most fundamental solution is change `where` in [dml.Insert](https://github.com/tobymao/sqlglot/blob/33de21fc21cdc05755a2de39318b292c10ccec0f/sqlglot/expressions/dml.py#L195) to something more general, like `replace`, and implement a method `parse_insert_replace` in the core parser, in this way, each dialect can implement their own "insert replace" parsing/generation.
But this solution introduces a breaking change.

I am new to sqlglot so just came up with the two solutions. Would like to hear some feedback from the team.

**Additional context**
Add any other context or screenshots about the feature request here.

