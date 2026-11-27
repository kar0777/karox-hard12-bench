You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

unlimited dims may cause the chunksize to exceed the shape

When opening a dataset with a coordinate along a unlimited dim the chunksize may be larger than the shape if we don't load the values of the variable into memory:

```python
import netCDF4

with netCDF4.Dataset("test.nc", mode="w") as f:
    dim_time = f.createDimension("time", None)
    var_time = f.createVariable("time", "i8", ("time",))
    var_time[:5] = 10

import virtualizarr

import xarray as xr
from obstore.store import LocalStore

from virtualizarr import open_virtual_dataset, open_virtual_mfdataset
from virtualizarr.parsers import HDFParser
from virtualizarr.registry import ObjectStoreRegistry

from pathlib import Path

store_path = Path.cwd()
file_path = str(store_path / "test.nc")
file_url = f"file://{file_path}"

store = LocalStore(prefix=store_path)
registry = ObjectStoreRegistry({file_url: store})

parser = HDFParser()
vds = open_virtual_dataset(
  url=file_url,
  parser=parser,
  registry=registry,
  loadable_variables=[],
)

vds["time"].data
```

This currently prints as
```
ManifestArray<shape=(5,), dtype=int64, chunks=(512,)>
```

The chunk shape comes from `h5py`:
```python
import h5py

with h5py.File("test.nc", mode="r") as f:
    print(f["time"].shape, f["time"].maxshape, f["time"].chunks)
```

This is a problem because it inhibits concatenation of virtual datasets or loading written (zarrquet) files.

<details><summary>versions</summary>

```
Environment: all
Package                Version                          Build                    Size       Kind   Source
aiohttp                3.12.15                                                   6.1 MiB    pypi   aiohttp-3.12.15-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
astropy                7.1.0                                                     34.5 MiB   pypi   astropy-7.1.0-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
codecov                2.1.13                                                    54.2 KiB   pypi   codecov-2.1.13-py2.py3-none-any.whl
dask                   2025.7.0                                                  5.6 MiB    pypi   dask-2025.7.0-py3-none-any.whl
fastparquet            2024.11.0                                                 7.5 MiB    pypi   fastparquet-2024.11.0-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
fsspec                 2025.7.0                                                  709.9 KiB  pypi   fsspec-2025.7.0-py3-none-any.whl
h5netcdf               1.6.4                            pyhd8ed1ab_0             47.3 KiB   conda  https://conda.anaconda.org/conda-forge/
h5py                   3.14.0                           nompi_py312h3faca00_100  1.3 MiB    conda  https://conda.anaconda.org/conda-forge/
hdf5                   1.14.6                           nompi_h6e4c0c1_103       3.5 MiB    conda  https://conda.anaconda.org/conda-forge/
hdf5plugin             5.1.0                                                     189.6 MiB  pypi   hdf5plugin-5.1.0-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
icechunk               1.1.4                                                     47.4 MiB   pypi   icechunk-1.1.4-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
imagecodecs            2025.8.2                                                  78.5 MiB   pypi   imagecodecs-2025.8.2-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl
imagecodecs_numcodecs  2024.6.1                                                  7.7 KiB    pypi   imagecodecs_numcodecs-2024.6.1-py3-none-any.whl
ipython                9.5.0                            pyhfa0c392_0             616 KiB    conda  https://conda.anaconda.org/conda-forge/
kerchunk               0.2.9                                                     205.1 KiB  pypi   kerchunk-0.2.9-py3-none-any.whl
lithops                3.6.1                                                     1.3 MiB    pypi   lithops-3.6.1-py3-none-any.whl
mypy                   1.17.1                                                    41.7 MiB   pypi   mypy-1.17.1-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl
netcdf4                1.7.2                            nompi_py312h3805cb1_102  1.1 MiB    conda  https://conda.anaconda.org/conda-forge/
numcodecs              0.16.2                                                    33.7 MiB   pypi   numcodecs-0.16.2-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
numpy                  2.3.2                            py312hf476fde_1          8 MiB      conda  https://conda.anaconda.org/conda-forge/
obstore                0.8.1                                                     9.9 MiB    pypi   obstore-0.8.1-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
packaging              25.0                             pyh29332c3_1             61 KiB     conda  https://conda.anaconda.org/conda-forge/
pandas_stubs           2.3.0.250703                                              615 KiB    pypi   pandas_stubs-2.3.0.250703-py3-none-any.whl
pooch                  1.8.2                                                     306.5 KiB  pypi   pooch-1.8.2-py3-none-any.whl
pre_commit             4.3.0                                                     363.1 KiB  pypi   pre_commit-4.3.0-py2.py3-none-any.whl
pytest                 8.4.1                                                     1.2 MiB    pypi   pytest-8.4.1-py3-none-any.whl
pytest_asyncio         1.1.0                                                     44.3 KiB   pypi   pytest_asyncio-1.1.0-py3-none-any.whl
pytest_cov             6.2.1                                                     74 KiB     pypi   pytest_cov-6.2.1-py3-none-any.whl
pytest_mypy            1.0.1                                                     21.1 KiB   pypi   pytest_mypy-1.0.1-py3-none-any.whl
pytest_xdist           3.8.0                                                     142.1 KiB  pypi   pytest_xdist-3.8.0-py3-none-any.whl
python                 3.12.11                          h9e4cc4f_0_cpython       30 MiB     conda  https://conda.anaconda.org/conda-forge/
requests               2.32.5                                                    199.5 KiB  pypi   requests-2.32.5-py3-none-any.whl
ruff                   0.12.10                                                   34.4 MiB   pypi   ruff-0.12.10-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
s3fs                   2025.7.0                                                  106.9 KiB  pypi   s3fs-2025.7.0-py3-none-any.whl
scipy                  1.16.1                                                    110.4 MiB  pypi   scipy-1.16.1-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.whl
ujson                  5.11.0                                                    121.1 KiB  pypi   ujson-5.11.0-cp312-cp312-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl
universal_pathlib      0.2.6                                                     171 KiB    pypi   universal_pathlib-0.2.6-py3-none-any.whl
virtualizarr           2.1.2.dev6+g2145ea496.d20250923                                      pypi    (editable)
xarray                 2025.8.0                                                  6.2 MiB    pypi   xarray-2025.8.0-py3-none-any.whl
zarr                   3.1.2                                                     1.1 MiB    pypi   zarr-3.1.2-py3-none-any.whl
```

</details>
