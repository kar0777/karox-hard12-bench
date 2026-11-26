You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Chart extraction: `_dataframe_to_tabledata` drops the header row whenever a series label is numeric (years, bins, indices)

**What happens.** The chart2csv output is read with `header=None`
(`granite_vision.py:338`), so the model's header line becomes row 0, and
`_dataframe_to_tabledata` (`:127-190`) decides whether row 0 is a header by

```python
first_row_is_header = all(not self._is_numeric(val) for val in first_row)   # :140
```

Any numeric label in that row — a year, a bin edge, a quarter number, or the `1, 2, 3`
the model emits when it cannot read the legend — makes `first_row_is_header` false. The
header row is then emitted as an ordinary data row with `column_header=False`, and the
grid has no column headers at all.

Concrete case: a bar chart classified at 0.999 came back as

```
Category,1,2,3,4
Institutional,85,15,0,0
Woodlot,10,60,30,0
...
```

Result: 9×5 grid, zero `column_header` cells. For the most common chart x-axis of all —
years — the same thing happens: `Region,2020,2021,2022` is rejected because three of
four labels are numbers.

A second, related issue on the body rows (`:172`):

```python
is_row_header = not self._is_numeric(value)
```

marks *every* non-numeric cell anywhere in the body as `row_header=True`, not only
column 0. A `n/a`, a `—`, or a text category in a middle column becomes a row header.

**Why it matters.** `column_header`/`row_header` are what downstream consumers use to
emit `<th>` / PDF `TH` + `Scope`, i.e. what makes the extracted table accessible. A
chart table with no header row is a grid of bare numbers to a screen-reader user, and
the failure is quietest exactly where charts are most regular.

**Suggested fix.** Two small changes, either sufficient for the common case:

1. Treat row 0 as the header when it is *mixed* (at least one non-numeric cell, e.g.
   `Category`), or when it is numeric but *monotone integer* (years/indices) and the body
   is not. Simpler still: the model is prompted for CSV *with* a header — trust row 0 as
   header unless it is entirely numeric **and** looks like data (same dtype as the rows
   below).
2. Restrict `row_header=True` to column 0 (or to the leading run of non-numeric columns),
   rather than any non-numeric cell.

Happy to open a PR with a unit test over `_dataframe_to_tabledata` covering the four
shapes (all-text header, mixed header, numeric-year header, text cell mid-body) if the
rule above is agreeable.

