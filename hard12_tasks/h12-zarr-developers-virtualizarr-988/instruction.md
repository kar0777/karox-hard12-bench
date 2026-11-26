You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Failure to read HDF5 data with data arrays of dtype='<U1'

Hello,
I am exploring VirtualiZarr/IceChunk for our workflow. I followed VirtualiZarr's example of reading one of our NetCDF files into VirtualiZarr:

```
import obstore
import virtualizarr as vz
from virtualizarr.parsers import HDFParser
from obspec_utils.registry import ObjectStoreRegistry

bucket = 's3://its-live-data'
granule = "velocity_image_pair/landsatOLI/v02/S80W170/LC08_L1GT_020121_20231013_20231102_02_T2_X_LC09_L1GT_020121_20231106_20231106_02_T2_G0120V02_P084.nc"

store = obstore.store.from_url(bucket, region="us-west-2", skip_signature=True)
registry = ObjectStoreRegistry({bucket: store})
parser = HDFParser()
# parser = HDFParser(drop_variables=['img_pair_info', 'mapping'])

vds = vz.open_virtual_dataset(
    url=f"{bucket}/{granule}",
    parser=parser,
    registry=registry,
    loadable_variables=[],
    
)
```

I'm getting the following failure:
```
virtualizarr/parsers/hdf/hdf.py:82
fill_value = dataset.fillvalue.item()
AttributeError: 'bytes' object has no attribute 'item'
```
It appears to be linked to the data variables of `string` dtype that don't have` _FillValue `attribute specified. Thinking it's a `_FillValue` issue, I added `_FillValue` attribute to our data and it failed with:

```
File [.../lib/python3.13/site-packages/xarray/backends/zarr.py:141](http://localhost:8888/...lib/python3.13/site-packages/xarray/backends/zarr.py#line=140), in FillValueCoder.encode(cls, value, dtype)
    139     return str(value)
    140 else:
--> 141     raise ValueError(f"Failed to encode fill_value. Unsupported dtype {dtype}")

ValueError: Failed to encode fill_value. Unsupported dtype object
```

Is it a bug or I'm doing something wrong?

If I exclude two "trouble" variables of string type (`parser = HDFParser(drop_variables=['img_pair_info', 'mapping'])`) when loading the data, the code works. 

After realizing that even if we get `img_pair_info` data read into the virtual dataset, we would not be able to preserve the attribute values we are interested in during the merge of all datasets into the virtual cube.
Is there a way to serialize data variable attributes into new variables of the virtual datacube when loading the data?I realize it can be done manually if `img_pair_info` is loaded into the virtual dataset — by extracting the attribute values and adding them as new data variables to the virtual dataset after calling `vz.open_virtual_dataset()`.

Is there a way to load the `mapping` into the datasets, but not to merge it as it's kind of a "constant" value that applies to all layers of the datacube?

I am using 
obstore 0.8.2
virtualizarr 2.4.0

Any advice would be greatly appreciated.

Thanks,
Masha



