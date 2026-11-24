You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

TemplateSpectralModel.to_dict() fails on big-endian arrays

**Gammapy version**
gammapy : 2.0.dev3689+g6f987f88e.d20260602
python_version: 3.12.13    
numpy : 2.4.6
astropy : 7.2.0

**Bug description**

`TemplateSpectralModel.to_dict()` raises `NotImplementedError` when the `energy` or `values` array is big-endian. This is the case for a model built from` crab_hess_fp.fits` , found this bug while testing ASDF serialization of `FluxPoints` from this file.

For a numpy array or `Quantity`, `.data` is a `memoryview` of the raw buffer and `memoryview` does not support non-native byte orders, So `to_dict()` fails if either `energy` or `values` is big-endian.

**To Reproduce**
```python 
import astropy.units as u
import numpy as np
from gammapy.modeling.models import TemplateSpectralModel

energy = np.array([1, 3, 10], dtype=">f8") * u.TeV
values = np.array([1e-11, 3e-12, 5e-13], dtype=">f8")

TemplateSpectralModel(energy=energy, values=values).to_dict()
```
Error:

```
File "gammapy/modeling/models/spectral.py", line 2141, in to_dict
    "data": self.energy.data.tolist(),
            ^^^^^^^^^^^^^^^^^^^^^^^^^
NotImplementedError: memoryview: unsupported format >d
```
**Other information**
Solution could be using `.value.tolist()` instead of `.data.tolist()` which works for any byte order.
