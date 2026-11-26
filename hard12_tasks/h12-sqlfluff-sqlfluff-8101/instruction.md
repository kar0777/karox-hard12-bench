You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

ClickHouse: GROUP BY ... WITH TOTALS / ROLLUP / CUBE modifiers are unparsable

### What happened

ClickHouse's `GROUP BY` modifiers `WITH TOTALS`, `WITH ROLLUP` and `WITH CUBE`
produce an unparsable section in the `clickhouse` dialect.

### Expected behaviour

The statements parse; the modifier is recognised as part of the `GROUP BY`
clause.

### Observed behaviour

```
L1:P37 PRS: Found unparsable section: 'WITH TOTALS'
```

(equivalently `WITH ROLLUP` / `WITH CUBE`)

### How to reproduce

```sql
SELECT a, count() FROM t GROUP BY a WITH TOTALS
SELECT a, count() FROM t GROUP BY a WITH ROLLUP
SELECT a, count() FROM t GROUP BY a WITH CUBE
```

```bash
sqlfluff parse --dialect clickhouse -
```

All three are valid and were verified on ClickHouse 26.4.2.
Docs: https://clickhouse.com/docs/sql-reference/statements/select/group-by

### Dialect

clickhouse

### Version

sqlfluff 4.2.2 (latest release), Python 3.12. Also applies to `main` — the only
change to the ClickHouse dialect grammar since 4.2.2 is the ternary operator
(#8016).

### Configuration

None — default rules, `--dialect clickhouse`.

