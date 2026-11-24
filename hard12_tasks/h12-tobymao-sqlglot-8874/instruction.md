You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Oracle: TO_DATE and TO_TIMESTAMP silently drop the nlsparam argument


With `read="oracle"`, the third argument (`nlsparam`) of `TO_DATE` and `TO_TIMESTAMP` is silently dropped:

```
input:  TO_DATE(c, 'DD-MON-YYYY', 'NLS_DATE_LANGUAGE = American')
output: TO_DATE(c, 'DD-MON-YYYY')
```

Oracle accepts up to three arguments (`char`, `fmt`, `nlsparam`), but sqlglot only keeps the first two, with no error or warning.

**Before you file an issue**
- Read dialect: `oracle`
- Write dialect: `oracle`
- Checked on main (6de2df31b), also reproduced on 30.18.0

**Fully reproducible code snippet**

The first two queries are the examples from the Oracle docs for `TO_DATE` and `TO_TIMESTAMP`.

```python
import sqlglot

for sql in [
    "SELECT TO_DATE('January 15, 1989, 11:00 A.M.', 'Month dd, YYYY, HH:MI A.M.', 'NLS_DATE_LANGUAGE = American') FROM DUAL",
    "SELECT TO_TIMESTAMP('10-Sep-02 14:10:10.123000', 'DD-Mon-RR HH24:MI:SS.FF', 'NLS_DATE_LANGUAGE = American') FROM DUAL",
    "SELECT TO_DATE(:p1, 'DD-MON-YYYY', :p2) FROM DUAL",
]:
    print(sqlglot.parse_one(sql, read="oracle").sql(dialect="oracle"))
```

Actual output:

```
SELECT TO_DATE('January 15, 1989, 11:00 A.M.', 'Month dd, YYYY, HH12:MI A.M.') FROM DUAL
SELECT TO_TIMESTAMP('10-Sep-02 14:10:10.123000', 'DD-Mon-RR HH24:MI:SS.FF') FROM DUAL
SELECT TO_DATE(:p1, 'DD-MON-YYYY') FROM DUAL
```

In all three cases the third argument is gone. Expected: it is kept, e.g. `TO_DATE('January 15, 1989, 11:00 A.M.', 'Month dd, YYYY, HH12:MI A.M.', 'NLS_DATE_LANGUAGE = American')`.

Dropping it changes what the query does. `nlsparam` sets the language used to read month and day names like `January` or `Sep`. Without it, Oracle falls back to the session's `NLS_DATE_LANGUAGE`, so the generated SQL can fail or behave differently on a session whose language isn't English.

**Official Documentation**

Both functions document the same signature:

```
TO_DATE(char [ DEFAULT return_value ON CONVERSION ERROR ] [, fmt [, 'nlsparam' ] ])
TO_TIMESTAMP(char [ DEFAULT return_value ON CONVERSION ERROR ] [, fmt [, 'nlsparam' ] ])
```

From the TO_DATE page: "The 'nlsparam' argument specifies the language of the text string that is being converted to a date." The TO_TIMESTAMP page says it "has the same purpose in this function as in the TO_CHAR function for date conversion."

- https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/TO_DATE.html
- https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/TO_TIMESTAMP.html

I have a fix ready and will open a PR shortly (prepared with help from Claude).
