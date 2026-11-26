You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

`SeqUtils.molecular_weight("")` returns +18.0153 instead of 0 or an error

The molecular weight of an empty sequence is not physically defined. But actual behavior is:

```python
>>> from Bio.SeqUtils import molecular_weight
>>> molecular_weight("", "DNA")
18.0153
>>> molecular_weight("", "RNA")
18.0153
>>> molecular_weight("", "protein")
18.0153
```

Suggested fix:

```python
if not seq:
    return 0.0
```

or raise `ValueError("sequence is empty")` if a zero-length input should be treated as invalid.
