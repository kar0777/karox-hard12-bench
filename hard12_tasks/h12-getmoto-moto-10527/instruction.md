You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

S3: get_object/head_object with PartNumber on a multipart object (whole object returned, KeyError for a missing part)

For an object completed from two parts (5 MiB + 1 KiB), with moto 5.2.5 and master dbe2556 in server mode:

```python
s3.get_object(Bucket=b, Key="mp", PartNumber=2)
# 200, 5243904 bytes starting with part 1, no ContentRange, no PartsCount
s3.get_object(Bucket=b, Key="mp", PartNumber=3)
# 200, the whole object again
s3.head_object(Bucket=b, Key="mp", PartNumber=2)
# 200, ContentLength 1024, PartsCount 2, no ContentRange
s3.head_object(Bucket=b, Key="mp", PartNumber=3)
# 500: KeyError: 3 in the server log
```

S3 answers a part request with 206, `Content-Range` for that part's bytes (`bytes 5242880-5243903/5243904` for part 2), `x-amz-mp-parts-count`, and only that part's body; a part number past the last part gets 416 `InvalidPartNumber`. Ranged downloads that fetch an object part by part (to match its multipart ETag, for example) read the wrong bytes against moto.

In `S3Response.get_object` the multipart branch is a `# TODO` that falls through to the full body. `head_object` gets the part's size right but sends no `Content-Range`, and it passes the part number to `S3Backend.get_object`, which looks it up with `key.multipart.parts[part_number]` and raises `KeyError` for a part that doesn't exist.

(The non-multipart case already returns 206 with `Content-Range`, and #7850 added PartNumber for regular keys.)

