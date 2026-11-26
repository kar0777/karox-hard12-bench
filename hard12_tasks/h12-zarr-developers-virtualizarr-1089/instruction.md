You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Forbid zero-length chunk references in ChunkManifest

## Proposal

`ChunkManifest` currently accepts entries with `length == 0` and a non-empty path. I think these should be rejected at construction time, because they are never a valid encoding of anything — they're always a parser bug.

### Why zero-length is always invalid

A Zarr chunk must decode to the full chunk shape. No codec pipeline emits 0 bytes for a chunk of a nonzero-size array — even an all-constant compressed chunk carries a codec header. And arrays with a zero-size dimension have no chunks at all. So there is no legitimate case that a `length == 0` check would break.

The correct representation for "this chunk isn't stored" already exists: `MISSING_CHUNK_PATH = ""`, which reads back as `fill_value` and issues no request at all.

### Where the gap is

Neither validation path checks it today:

- `validate_byte_range` (`virtualizarr/manifests/manifest.py`) only checks `length >= 0`.
- `ChunkManifest.from_arrays` doesn't check lengths at all.

Icechunk *does* reject these, but only on read — so a bad reference gets durably committed and fails months later:

```
InvalidInputError: byte range From(0) is out of bounds for chunk of length 0
```

Reading through `ManifestStore` fails similarly with `ValueError: Invalid range requested, start: 0 end: 0`.

### Motivating case: sparse COGs

Sparse GeoTIFFs (GDAL `SPARSE_OK=TRUE`) store nothing for empty tiles, writing `offset = 0, byteCount = 0` in `TileOffsets`/`TileByteCounts`. This is common in practice — [one recent example](https://github.com/kentstephen/x-sql-marimo) reports 73.6% of full-resolution tiles being sparse in a global forest-loss COG, because ocean simply isn't stored.

Our recommended TIFF parser currently emits a real reference for every one of those tiles. Repro with a sparse tiled TIFF (tile 0 written, tiles 1–3 skipped):

```python
offsets              lengths
[[304   0]           [[65536     0]
 [  0   0]]           [    0     0]]
```

All four chunks reference the file; writing to Icechunk succeeds, and the read then fails. Masking the paths where `lengths == 0` fixes it completely — real data preserved, sparse tiles return `fill_value`, and no request is issued for them:

```python
paths[m._lengths == 0] = ""   # -> read OK, unique values: [0 7], fill_value: 0
```

That parser fix belongs in [virtual-tiff](https://github.com/virtual-zarr/virtual-tiff) and I'll open it separately. This issue is about VirtualiZarr catching the class of mistake so it can't reach a store — and so the failure surfaces at parse time rather than at read time after a commit.

### Cost

One vectorized check, `(lengths == 0) & (paths != MISSING_CHUNK_PATH)`, over the arrays. Negligible even on the `validate_paths=False` fast path that parsers use for performance.

### Scope

- `ChunkManifest.from_arrays` — vectorized check
- `ChunkEntry.with_validation` / `validate_byte_range` — scalar check
- Possibly worth mirroring in Icechunk's virtual-ref *write* path, so non-VirtualiZarr writers can't plant one either — but that's a separate upstream conversation.

