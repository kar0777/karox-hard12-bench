You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

docs: use actual lowercase parameter names in error messages

Some user-facing error messages refer to parameters by uppercase MATLAB/QETLAB-style names (`PHI`, `DIM`) instead of the actual lowercase Python parameter names (`phi`, `dim`). This is confusing: a user who hits the error cannot map `PHI` to any argument they passed.

### What to do
Update the messages to use the real parameter names.

- `toqito/channel_props/channel_dim.py` — four messages using `PHI`/`DIM`, e.g. `"The input and output spaces of PHI must be square."` becomes `` "The input and output spaces of `phi` must be square." ``
- `toqito/perms/permute_systems.py` — the message mentioning `DIM` and `X`.
- `toqito/states/horodecki.py` — `"InvalidDim: DIM must be one of [3, 3], or [2, 4]."` becomes `dim`.

Find them with:
```
git grep -nE "PHI|DIM" toqito/channel_props/channel_dim.py toqito/perms/permute_systems.py toqito/states/horodecki.py
```

### Note
Some tests assert on these exact strings via `pytest.raises(..., match=...)`; update those matches too. Then run:
```
uv run pytest toqito/channel_props/tests/test_channel_dim.py toqito/perms/tests toqito/states/tests/test_horodecki.py
```

