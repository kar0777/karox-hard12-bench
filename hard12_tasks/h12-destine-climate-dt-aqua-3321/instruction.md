You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[Regridder] Regridded field shifted by 180° in longitude for lon-lat sources stored on [-180, 180]

## Summary

Since the longitude `range_convention: "0_to_360"` of the `aqua` data model (introduced in
efcb97b09, first released in v1.2.0), `Reader.regrid()` returns a field shifted by 180° in
longitude for any global regular lon-lat source stored on [-180, 180). The coordinates of
the output are correct, the values are not: e.g. MSWEP July precipitation regridded to
r100 puts about 2.6 mm/day over the Sahara (native value 0).

Checked with AQUA 1.2.3 (`main` at 999c9e31c, 2026-10-30) on LUMI. Affected sources found:

- `obs` `MSWEP` `v2.8` `monthly-zarr` and `monthly-netcdf` (stored on [-179.95, 179.95]);
- `obs` `BERKELEY-EARTH` `aqua-filled` `r100-monthly` and `r025-monthly` (stored on [-179.5, 179.5] / [-179.875, 179.875]).

Not affected: ERA5 (stored on [0, 360)) and E-OBS (regional, the wrap is skipped by the
safety check in `normalize_range_convention`).

## Cause

1. `CoordTransformer.normalize_range_convention` wraps the longitudes into [0, 360) and
   `sortby(lon)`, i.e. it rolls the data along `lon` by half the domain.
2. The regridding weights are generated from the grid as stored (via `_retrieve_plain`,
   [-180, 180) order); `_fix_datamodel_weights` applies the data model with
   `flip_coords=False` to the weight coordinates only.
3. Before regridding, `Reader.regrid` calls `counter_reverse_coordinate`, which undoes only
   coordinates carrying the `flipped` attribute (latitude), not the longitude wrap/sort.
4. smmregrid applies the weights by flattened index, so the source cells are read in the
   wrong longitude order.

## Reproduce

Compares `Reader.regrid()` to r100 with a 1° box mean of the native data (the 0.1°/0.25°
cell edges align with the r100 cells, so the box mean is a conservative remap), with and
without the data model.

```python
import warnings

import numpy as np
import aqua
from aqua import Reader

warnings.filterwarnings("ignore")
print("AQUA", aqua.__version__)

CASES = [
    dict(catalog="obs", model="MSWEP", exp="v2.8", source="monthly-zarr", var="tprate", factor=10),
    dict(catalog="obs", model="BERKELEY-EARTH", exp="aqua-filled", source="r025-monthly", var="2t", factor=4),
    dict(catalog="obs", model="BERKELEY-EARTH", exp="aqua-filled", source="r100-monthly", var="2t", factor=1),
]


def corr(a, b):
    a, b = a.values.ravel(), b.values.ravel()
    ok = np.isfinite(a) & np.isfinite(b)
    return np.corrcoef(a[ok], b[ok])[0, 1]


def rms(a, b):
    return float(np.sqrt(((a - b) ** 2).mean()))


def check(case, datamodel):
    kwargs = {} if datamodel else {"datamodel": False}
    reader = Reader(catalog=case["catalog"], model=case["model"], exp=case["exp"], source=case["source"],
                    regrid="r100", startdate="2017-07-01", enddate="2017-07-31", loglevel="ERROR", **kwargs)
    native = reader.retrieve(var=case["var"])[case["var"]].isel(time=0)
    regridded = reader.regrid(native).load()
    # without the data model the coordinates keep their stored names
    native = native.rename({c: n for c, n in (("latitude", "lat"), ("longitude", "lon")) if c in native.dims})
    lon_range = f"[{float(native.lon.min()):.2f}, {float(native.lon.max()):.2f}]"
    box = native.sortby("lat").sortby("lon").coarsen(lat=case["factor"], lon=case["factor"]).mean().load()
    box = box.assign_coords(lon=(box.lon % 360)).sortby("lon")
    box = box.assign_coords(lat=regridded.lat, lon=regridded.lon)  # same cells, rounding only
    rolled = box.roll(lon=180, roll_coords=False)
    print(f"{case['model']:15s} {case['source']:13s} datamodel={str(datamodel):5s} lon after retrieve {lon_range:18s} "
          f"regrid vs box mean: corr {corr(regridded, box):.3f} RMS {rms(regridded, box):.3g} | "
          f"vs box mean rolled 180 deg: corr {corr(regridded, rolled):.3f} RMS {rms(regridded, rolled):.3g}")


for case in CASES:
    for datamodel in (True, False):
        check(case, datamodel)
```

### Output 

LUMI, AQUA 1.2.3, smmregrid 0.2.0; units: MSWEP kg m-2 s-1, Berkeley Earth K

```
MSWEP           monthly-zarr  datamodel=True  lon after retrieve [0.05, 359.95]     regrid vs box mean: corr 0.257 RMS 4.26e-05 | vs box mean rolled 180 deg: corr 0.989 RMS 5.11e-06
MSWEP           monthly-zarr  datamodel=False lon after retrieve [-179.95, 179.95]  regrid vs box mean: corr 0.989 RMS 5.11e-06 | vs box mean rolled 180 deg: corr 0.257 RMS 4.26e-05
BERKELEY-EARTH  r025-monthly  datamodel=True  lon after retrieve [0.12, 359.88]     regrid vs box mean: corr 0.925 RMS 8.73 | vs box mean rolled 180 deg: corr 1.000 RMS 0.498
BERKELEY-EARTH  r025-monthly  datamodel=False lon after retrieve [-179.88, 179.88]  regrid vs box mean: corr 1.000 RMS 0.498 |vs box mean rolled 180 deg: corr 0.925 RMS 8.73
BERKELEY-EARTH  r100-monthly  datamodel=True  lon after retrieve [0.50, 359.50]     regrid vs box mean: corr 0.925 RMS 8.72 | vs box mean rolled 180 deg: corr 1.000 RMS 0.456
BERKELEY-EARTH  r100-monthly  datamodel=False lon after retrieve [-179.50, 179.50]  regrid vs box mean: corr 1.000 RMS 0.456 |vs box mean rolled 180 deg: corr 0.925 RMS 8.72
```

With the default data model the regridded field matches the box mean **rolled by 180°**;
with `datamodel=False` it matches the box mean. For temperature the correlation stays high
(0.925) because of the meridional gradient, so the error is easy to miss; the RMS error is
8.7 K.

**Impact**

Any bias/climatology against these references computed with AQUA >= 1.2.0 (e.g. the AQUA
Biases diagnostic with MSWEP or Berkeley Earth as reference) is wrong.

It is not a stale weights/areas problem: with `Reader(..., rebuild=True)` the weights are
regenerated (new files on 2026-11-02 with AQUA 1.2.3) and the result is identical:

```
MSWEP           monthly-zarr  datamodel=True  rebuild=True  regrid vs box mean: corr 0.257 RMS 4.26e-05 | vs box mean rolled 180 deg: corr 0.989 RMS 5.11e-06
BERKELEY-EARTH  r100-monthly  datamodel=True  rebuild=True  regrid vs box mean: corr 0.925 RMS 8.72 | vs box mean rolled 180 deg: corr 1.000 RMS 0.456
```

The weights follow the stored grid, which is consistent; the data passed to them are not.

## Workaround

Read the reference with `datamodel=False` (in a diagnostic config:
`reader_kwargs: {datamodel: false}` in the reference entry). The regridded output is on the
target grid in [0, 360) anyway.

## Possible fix

Undo the longitude wrap/sort before `regrid` (as `counter_reverse_coordinate` does for the
latitude flip, e.g. mark the wrapped coordinate and restore the stored order), or build the
weights from the data after the data model has been applied.
