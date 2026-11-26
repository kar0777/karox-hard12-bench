You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

`Dataset.compress()` produces byte-swapped pixel data when source Transfer Syntax is Explicit VR Big Endian


## Description

`Dataset.compress()` silently produces corrupted (byte-swapped) pixel data when compressing a dataset whose Transfer Syntax is Explicit VR Big Endian (`1.2.840.10008.1.2.2`). The resulting compressed file contains pixel values with swapped byte order, where a 16-bit value of `1` (`0x0001`) becomes `256` (`0x0100`).

The corruption is silent: no error, no warning. For lossless compression (JPEG 2000 Lossless), the round-trip pixel data does not match the original.

We're aware that Explicit VR Big Endian was retired from the DICOM Standard in 2006 (Supplement 98) and that conformant implementations are not required to support it. However, Big Endian files still exist in the wild, including legacy PACS exports and long-running research datasets hosted on platforms like [IDA/LONI](https://ida.loni.usc.edu). Since pydicom does read these files (and `pixel_array` decodes them correctly), we'd expect `compress()` to handle them as well.

## Cause

When no `arr` argument is passed, `compress()` appears to read the raw `PixelData` bytes without accounting for the source transfer syntax endianness. On a little-endian host the big-endian bytes are fed directly to the encoder, which interprets them as little-endian.

## Workaround

Passing `arr=ds.pixel_array` explicitly forces `compress()` through the pixel decoding pipeline, which correctly handles the `>u2` / `>i2` dtype:

```python
ds = pydicom.dcmread("bigendian_file.dcm")
ds.compress(JPEG2000Lossless, arr=ds.pixel_array, encoding_plugin="pylibjpeg")
```

This is not documented as a requirement. The [compression tutorial](https://github.com/pydicom/pydicom/blob/main/doc/tutorials/pixel_data/compressing.rst) only shows `arr` being used for creating new datasets or updating pixel data, not as a mandatory workaround for Big Endian sources. It's worth noting that `compress()` is a method on the very `Dataset` that already holds the correctly decoded `pixel_array`, so having to pass it back in explicitly to avoid silent corruption is surprising.

## Reproducer

Uses a public Big Endian DICOM from [neurolabusc/dcm_qa_ts](https://github.com/neurolabusc/dcm_qa_ts/blob/main/In/3.dcm):

```python
import numpy as np
import pydicom
from pydicom.filewriter import dcmwrite
from pydicom.uid import JPEG2000Lossless

ds = pydicom.dcmread("3.dcm")  # Explicit VR Big Endian
original_pixels = ds.pixel_array.copy()

# Compression yields neither error nor warning
ds.compress(JPEG2000Lossless, generate_instance_uid=False)
dcmwrite("/tmp/compressed.dcm", ds)

# Round-trip check — FAILS
ds_comp = pydicom.dcmread("/tmp/compressed.dcm")
np.testing.assert_array_equal(original_pixels, ds_comp.pixel_array)
# AssertionError: Mismatched elements: 140956 / 147456 (95.6%)
```

## Environment

- pydicom 3.0.2
- Python 3.11
- Platform: little-endian (x86_64)
