You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

private_block() returns a stale block after the private creator is removed with pop() or clear()

**Describe the bug**
This is #1097 again, through a different path. The fix for that issue resets the private block cache in `__delitem__`, but `Dataset.pop()`, `popitem()` and `clear()` remove elements without going through `__delitem__`, so the cache survives. The next `private_block(..., create=True)` returns the old block and doesn't add the private creator back, so you end up with private data elements that have no (gggg,00xx) creator.

Overwriting the private creator element with a different creator has the same problem: `private_block()` still finds the old creator.

**Expected behavior**
The same as after `del ds[0x000B0010]`. Recreating the block adds the private creator again, and looking up a creator that is no longer in the dataset raises `KeyError`.

**Steps To Reproduce**
Using the example from #1097:

```python
from pydicom import Dataset

ds = Dataset()
block = ds.private_block(0x000B, "dog^1", create=True)
block.add_new(0x01, "SH", "Border Collie")

ds.clear()
block = ds.private_block(0x000B, "dog^1", create=True)
block.add_new(0x01, "SH", "Poodle")
print(ds)
```

```
(000B,1001) Private tag data                    SH: 'Poodle'
```

There's no `(000B,0010) Private Creator` element. `ds.pop(0x000B0010)` in place of `clear()` gives the same result.

Replacing the creator:

```python
from pydicom import Dataset
from pydicom.dataelem import DataElement

ds = Dataset()
ds.private_block(0x000B, "dog^1", create=True)
ds[0x000B0010] = DataElement(0x000B0010, "LO", "cat^1")
ds.private_block(0x000B, "dog^1")
```

This returns a block for (000B,10xx) instead of raising `KeyError`, even though that block now belongs to `cat^1`.

**Your environment**
main at a6374203fe

```
module       | version
------       | -------
platform     | macOS-27.0.1-arm64-arm-64bit
Python       | 3.12.13 (main, May 10 2026, 19:20:41) [Clang 22.1.3 ]
pydicom      | 3.1.0.dev0
gdcm         | _module not found_
jpeg_ls      | _module not found_
numpy        | 2.5.4
PIL          | _module not found_
pylibjpeg    | _module not found_
openjpeg     | _module not found_
libjpeg      | _module not found_
```

