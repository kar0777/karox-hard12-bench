You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Values that do not fit the declared dtype are silently wrapped on input

An `Array[..., Int8]` input given `[300]` validates and comes out as `[44]`. Same for the json-encoded path (`{"dtype": "int8", "data": {"buffer": [300], "encoding": "json"}}` gives `[44]`), and `Float32` given `1e40` becomes `inf`. NumPy prints a `RuntimeWarning: overflow encountered in cast` and the request succeeds.

The `same_kind` check in `_coerce_shape_dtype` only compares kinds, so int64 -> int8 passes and the `astype` wraps; the json branch in `decode_array` casts with `casting="unsafe"` after checking for fractional parts but not for range.

Fractional floats into an integer field are already rejected ("Expected integer data"), so rejecting out-of-range values in the same place seems consistent. Happy to open a PR.

Checked on main (b950c98), numpy 2.5.2.
