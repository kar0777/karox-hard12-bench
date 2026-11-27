You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

`.gradient()` returns only one non-NaN value on ne120np4 grid

### Version

2025.12.0

### How did you install UXarray?

Conda

### What happened?

All values returned by public function `gradient()` and private function `_compute_gradient()` are NaN, except at index 776887.

xarray 2024.11.0
numpy 1.26.4
numba 0.61.0

### What did you expect to happen?

Zonal and meridional gradient arrays with no NaN values

### Can you provide a MCVE to repoduce the bug?

```python
import uxarray as ux
import xarray as xr
import numpy as np

FILI = '/glade/work/jpan/ux_grad_nan/ne120np4_testdata.nc'
UGRD = '/glade/p/cesmdata/inputdata/share/scripgrids/ne120np4_pentagons_100310.nc'

uxds = ux.open_dataset(UGRD, FILI)
grad_zon, grad_mer = ux.core.gradient._compute_gradient(uxds['U200'].squeeze())
notnan = ~np.isnan(grad_mer)
print('Results for private function')
print(sum(notnan))
print(np.where(notnan))

gradds = uxds['U200'].squeeze().gradient()
notnan = ~np.isnan(gradds['meridional_gradient'])
print('\nResults for public function')
print(sum(notnan))
print(np.where(notnan))
```
