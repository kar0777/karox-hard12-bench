You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

codify fails or writes invalid code for multi-valued AT/PN elements and empty values

**Describe the bug**

`pydicom codify` (and `pydicom.util.codify.code_dataelem()`) fails, or produces Python code that doesn't run, for some common element values:

1. Multi-valued **AT** elements raise `AttributeError: 'MultiValue' object has no attribute 'group'`. *Frame Increment Pointer* in multi-frame files usually has more than one value, so this happens with the bundled `JPGExtended.dcm`:

   ```
   $ pydicom codify pydicom::JPGExtended.dcm
   ...
     File ".../pydicom/util/codify.py", line 50, in tag_repr
       return f"(0x{tag.group:04X}, 0x{tag.element:04X})"
   AttributeError: 'MultiValue' object has no attribute 'group'
   ```

   An empty **AT** element (value `None`) fails in the same place.

2. With `exclude_size` set (the CLI default is 100), an empty binary element raises `TypeError: object of type 'NoneType' has no len()`. The bundled `reportsi_with_empty_number_tags.dcm` has an empty *Vector Grid Data* (OF) and fails like this:

   ```
   $ pydicom codify pydicom::reportsi_with_empty_number_tags.dcm
   ...
     File ".../pydicom/util/codify.py", line 135, in code_dataelem
       and len(dataelem.value) > exclude_size
   TypeError: object of type 'NoneType' has no len()
   ```

3. Multi-valued **PN** elements and empty multi-valued elements produce code that isn't valid Python, because the `MultiValue` repr is used as-is:

   ```python
   from pydicom.dataelem import DataElement
   from pydicom.util.codify import code_dataelem

   print(code_dataelem(DataElement(0x00101001, "PN", ["Doe^John", "Roe^Jane"])))
   # ds.OtherPatientNames = [Doe^John, Roe^Jane]   -> NameError when run
   print(code_dataelem(DataElement(0x00080008, "CS", [])))
   # ds.ImageType =                                 -> SyntaxError when run
   ```

   Multi-valued PN is common, e.g. *Other Patient Names*, *Operators' Name* or *Performing Physician's Name*.

**Expected behavior**

```
ds.FrameIncrementPointer = [(0x0054, 0x0010), (0x0054, 0x0020)]
ds.VectorGridData = None
ds.OtherPatientNames = ['Doe^John', 'Roe^Jane']
ds.ImageType = []
```

**Your environment**

module       | version
------       | -------
platform     | macOS-27.0.1-arm64-arm-64bit
Python       | 3.12.13
pydicom      | 3.1.0.dev0 (main, 7aa88629)
numpy        | 2.5.4

