You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

StringLiteral to IntegerType/LongType silently truncates fractional strings, changing predicate meaning

### Apache Iceberg version

0.12.0 (latest release)

### Please describe the bug 🐞

`literal("2.6").to(IntegerType())` returns `LongLiteral(2)` instead of raising, while `DecimalLiteral(Decimal("2.6")).to(IntegerType())` raises ValueError. A bound predicate such as `x < "2.6"` on an int column therefore becomes `x < 2` and wrongly drops rows with x = 2 (verified with `expression_evaluator`); the same bound literal feeds partition pruning, so files can be skipped too.

The sibling `DecimalLiteral.to(IntegerType/LongType)` already rejects fractional values via the existing `_to_integral` helper, with a test spelling out why: rounding would change the predicate (e.g. x > 2.6 becoming x > 3 drops x = 3). The StringLiteral path was missed. The reference Java implementation has no INTEGER/LONG case in `StringLiteral.to()` and refuses the conversion.

Suggested fix: use the existing `_to_integral` helper in both `StringLiteral.to(IntegerType)` and `StringLiteral.to(LongType)`, and update `test_string_literal` to expect ValueError for fractional strings.

Reproduction (pyiceberg 0.12.0, main @ fce8185):
- `literal("2.6").to(IntegerType())` returns `LongLiteral(2)`; same for LongType
- `literal("-2.5").to(IntegerType())` returns `LongLiteral(-2)`; `literal("0.1").to(LongType())` returns `LongLiteral(0)`
- `LessThan("x", "2.6")` bound to an int column becomes `x < 2`, and `expression_evaluator` returns False for a row with x = 2, although x < 2.6 is True
- Integral strings still convert exactly: `literal("2.0").to(IntegerType())` returns 2, `literal("1e3").to(IntegerType())` returns 1000

### Willingness to contribute

- [x] I can contribute a fix for this bug independently
- [ ] I would be willing to contribute a fix for this bug with guidance from the Iceberg community
- [ ] I cannot contribute a fix for this bug at this time
