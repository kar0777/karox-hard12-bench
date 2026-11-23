You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

PersonName.from_named_components replaces non-ASCII str components with '?' unless encodings are passed

**Describe the bug**
`PersonName.from_named_components()` encodes the given components when it is called, using the default ISO-8859-1 encoding if `encodings` is not given. Non-ASCII ideographic or phonetic components passed as `str` are replaced with `?` (with a "Failed to encode value with encodings: iso8859" warning), and the loss is permanent: the dataset's *Specific Character Set* has no effect when the element is written, because the `PersonName` already holds the lossy bytes with `encodings=None`. Assigning the same name as a plain `str` works correctly. `from_named_components_veterinary()` behaves the same way.

**Expected behavior**
Components given as `str` should be kept decoded and encoded when the element is written, using the dataset's *Specific Character Set*, exactly as for `ds.PatientName = "Yamada^Tarou=山田^太郎"`.

**Steps To Reproduce**
```python
import io
from pydicom import Dataset, dcmread, dcmwrite
from pydicom.dataset import FileMetaDataset
from pydicom.uid import ExplicitVRLittleEndian
from pydicom.valuerep import PersonName

ds = Dataset()
ds.file_meta = FileMetaDataset()
ds.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian
ds.file_meta.MediaStorageSOPClassUID = "1.2.3"
ds.file_meta.MediaStorageSOPInstanceUID = "1.2.3.4"
ds.SpecificCharacterSet = ["", "ISO 2022 IR 87"]

ds.PatientName = PersonName.from_named_components(
    family_name="Yamada", given_name="Tarou",
    family_name_ideographic="山田", given_name_ideographic="太郎",
    family_name_phonetic="やまだ", given_name_phonetic="たろう",
)
print(ds.PatientName.ideographic)   # ??^??

buffer = io.BytesIO()
dcmwrite(buffer, ds, enforce_file_format=True)
buffer.seek(0)
print(dcmread(buffer).PatientName)  # Yamada^Tarou=??^??=???^???

ds.PatientName = "Yamada^Tarou=山田^太郎=やまだ^たろう"
buffer = io.BytesIO()
dcmwrite(buffer, ds, enforce_file_format=True)
buffer.seek(0)
print(dcmread(buffer).PatientName)  # Yamada^Tarou=山田^太郎=やまだ^たろう
```

**Your environment**
- pydicom 3.1.0.dev0 (main, db6c2f5775)
- Python 3.12.13
- macOS (Darwin 27.2.0)

