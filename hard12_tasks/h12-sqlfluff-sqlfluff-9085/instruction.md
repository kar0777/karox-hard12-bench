You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Bug: -- noqa: disable=PRS,ALL behaves differently by OS

### Search before asking

- [x] I searched the [issues](https://github.com/sqlfluff/sqlfluff/issues) and found no similar issues.


### What Happened

The same file, with the same config and sqlfluff version, lints differently on Windows and Linux when a `noqa` comment lists `ALL` (uppercase) together with other codes:

* Windows: `ALL` expands to every rule, so all violations in the range are suppressed.
* Linux: `ALL` doesn't expand. It's kept as a literal, unknown code, so only the other listed codes are suppressed.

As a result, a file passes on a Windows dev machine and fails in a Linux CI job.

### Expected Behaviour

The same `noqa` comment should behave the same on every OS. Since the docs write rule codes in uppercase and the `all` group in lowercase, matching should most likely be case-insensitive everywhere.

### Observed Behaviour

`-- noqa: disable=PRS,ALL` ignores all rule violations on Windows and only disables parsing on Linux.

### How to reproduce

Create file `upper.sql`:

```sql
-- noqa: disable=PRS,ALL
SELECT a   AS b FROM t
-- noqa: enable=PRS,ALL
```

Lint it:

```shell
sqlfluff lint --dialect ansi --rules LT01 upper.sql
```

File | Windows | Linux
-- | -- | --
upper.sql (above) | passes | LT01 reported
inline: SELECT a AS b FROM t -- noqa: PRS,ALL | passes | LT01 reported
lowercase list: disable=PRS,all / enable=PRS,all | passes | passes
bare: disable=all / enable=all | passes | passes

Tested with sqlfluff 4.5.0 on Windows 11 and Ubuntu 22.04, on Python 3.10, 3.11, and 3.13, with and without `sqlfluffrs`. The raw violations with `--disable-noqa` are identical on both platforms; only the suppression differs.

Dumping `LintedFile.ignore_mask` for the same `-- noqa: disable=PRS,ALL` comment shows the difference directly:

```
Windows: action=disable rules=['AL01', 'AL02', …, 'TQ04']   # ALL expanded
Linux:   action=disable rules=['ALL', 'PRS']               # 'ALL' kept as a literal code
```

**Cause?**

`src/sqlfluff/core/rules/noqa.py` (around line 123 in 4.5.0) expands each listed code with `fnmatch.filter`:

```python
for x in fnmatch.filter(reference_map.keys(), r)
```

`fnmatch.filter` / `fnmatch.fnmatch` normalize case with `os.path.normcase`, so they're case-insensitive on Windows and case-sensitive on POSIX. The `reference_map` key for the group is lowercase `all`, so `ALL` matches it only on Windows. The bare `disable=all` form doesn't hit this, because it's handled before the glob expansion (`if rule_part != "all"`).

The same applies to any other code, group name, or glob written in a different case from its `reference_map` key, for example `layout` vs `LAYOUT`.

**Possible fix**

Make the matching OS-independent and case-insensitive. For example, lower-case both sides and use `fnmatch.fnmatchcase`, or compare against a lower-cased copy of the `reference_map` keys. A unit test that patches `os.path.normcase` (or runs the existing `noqa` tests on both OSes) would catch regressions.

### Dialect

ANSI

### Version

Tested with sqlfluff 4.5.0 on Windows 11 and Ubuntu 22.04, on Python 3.10, 3.11, and 3.13, with and without `sqlfluffrs`.

### Configuration

Reproduces with default configs.

### Are you willing to work on and submit a PR to address the issue?

- [x] Yes I am willing to submit a PR!

### Code of Conduct

- [x] I agree to follow this project's [Code of Conduct](https://github.com/sqlfluff/sqlfluff/blob/main/CODE_OF_CONDUCT.md)

