You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

HDFParser: read variable-length string datasets at parse time as inlined chunks

Split out of #1104, as @TomNicholas suggested there.

### Problem

`HDFParser` can't read HDF5 variable-length string datasets. Their chunks hold pointers into the HDF5 global heap, not the strings, so a virtual reference to them can't be decoded. Today the parser warns and virtualizes the metadata anyway. Reading the variable then fails, and so does `loadable_variables`, which reads the same chunks:

```python
with h5py.File("/tmp/strings.h5", "w") as f:
    f["labels"] = np.array(["a", "bb", "ccc"], dtype=h5py.string_dtype())

parse("/tmp/strings.h5", loadable_variables=["labels"])
# UserWarning: Variable '/labels' is an HDF5 variable-length string dataset. ...
# ValueError: corrupt buffer, data seem truncated
```

The only workaround is to find these datasets with h5py first, pass them to `drop_variables`, and read and write them separately. In some formats they're everywhere: every NWB file has several, for example.

### Proposal

Read the strings at parse time and store them as inlined chunks:

- Read each HDF5 chunk with h5py, using the HDF5 chunk shape trimmed to the array shape. Encode it the way Zarr's `vlen-utf8` codec does, padding an edge chunk with the fill value.
- Use `vlen-utf8` as the only codec. The HDF5 filters compress the heap pointers, not the strings.
- Keep an empty manifest for a dataset with no allocated storage, so it reads as the fill value.

`ChunkManifest` already supports inlined chunks, and the Icechunk and kerchunk writers already write them.

One related fix is needed for the kerchunk writer. `convert_v3_to_v2_metadata` drops every array-to-bytes codec, including `vlen-utf8`. A Zarr v2 string array needs `vlen-utf8` as its first filter, so a string array written to kerchunk currently can't be read.

I have a PR for this ready.

