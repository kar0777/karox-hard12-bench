You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

BgzfWriter raises struct.error or placeholder RuntimeError on incompressible data

`BgzfWriter.write()` splits input into 65536-byte blocks. If a block doesn't compress (e.g. random or already-compressed data), `_write_block` fails in one of two ways:

- Block sizes of about 65,491 to 65,516 bytes of random data raise `struct.error: 'H' format requires 0 <= number <= 65535`, because BSIZE is stored as `len(compressed) + 25` in a 16-bit field.
- About 65,517 to 65,536 bytes raise `RuntimeError: TODO - Didn't compress enough, try less data in this block`.

**Reproduction**

```python
import io, random
from Bio import bgzf

w = bgzf.BgzfWriter(fileobj=io.BytesIO(), mode="wb")
w.write(random.Random(42).randbytes(65536))
w.close()   # RuntimeError: TODO - Didn't compress enough...
```

With `randbytes(65500)` the failure is the `struct.error` instead (raised from `close()` -> `flush()` -> `_write_block`).

**Cause**

The guard in `_write_block` checks `len(compressed) > 65536`, but because of the 26 bytes of header/footer and the 16-bit BSIZE field, the compressed data must be at most about 65510 bytes. Compressed sizes between 65511 and 65536 get past the guard and then fail in `struct.pack("<H", ...)`.

**Environment**

Reproduced on current master (1.89.dev0, commit 49fefbc), Python 3.12.3, Linux.

**Notes**

- Other BGZF writers avoid this by limiting the uncompressed block size (htslib uses 0xff00 bytes, as I understand it) or by retrying with less input.
- There is no existing test in `Tests/test_bgzf.py` for incompressible data.
- Minor: `flush()` slices 65535 bytes while `write()` slices 65536, and `crc` in `_write_block` is computed twice (the first computation is dead code).

I'd like to work on a fix and a regression test myself. Would maintainers prefer a smaller fixed block size or a retry approach?
