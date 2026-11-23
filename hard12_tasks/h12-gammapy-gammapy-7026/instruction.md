You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Failing FluxPointsEstimator because of UL scan

**Gammapy version**
dev

**Bug description**
FluxPointsEstimator sometimes fails with:`ValueError: MapAxis: node values must be unique`
even though no axis actually has duplicated nodes. A recent occurence is in the gammapy-benchmarks `fermi-3fhl` validation,  see [log](https://github.com/gammapy/gammapy-benchmarks/actions/runs/43280161585/job/131399019076)

```
  File ".../gammapy/estimators/points/sed.py", line 233, in run
    return FluxPoints.from_table(
  File ".../gammapy/estimators/points/core.py", line 417, in from_table
    maps[name] = RegionNDMap.from_table(
  File ".../gammapy/maps/region/ndmap.py", line 614, in from_table
    axes = MapAxes.from_table(table=table, format=format)
  File ".../gammapy/maps/axes.py", line 2151, in from_table
    axis = MapAxis.from_table(table=table, format=axis_format)
  File ".../gammapy/maps/axes.py", line 1450, in from_table
    axis = MapAxis.from_nodes(nodes, name="norm")
  File ".../gammapy/maps/axes.py", line 710, in from_nodes
    return cls(nodes, node_type="center", **kwargs)
  File ".../gammapy/maps/axes.py", line 137, in __init__
    raise ValueError("MapAxis: node values must be unique")
```

**Expected behavior**
The issue is likely caused by the new behaviour regarding failing ULs. Here is a diagnostic obtained with Claude.
 
- With `selection_optional=["ul"]`, `ParameterEstimator` still runs a likelihood scan as a fallback when the UL from `Fit.confidence` is invalid 
- So only the energy bins whose UL failed get `norm_scan` / `stat_scan` keys in their result dict.
- `FluxPointsEstimator.run` builds `Table(rows, ...)`. For rows without these keys, astropy fills in masked values in a `MaskedColumn`.
- `MapAxis.from_table(format="gadf-sed-norm")` builds the norm axis from row 0 only: `flat_if_equal(table["norm_scan"][0])`. If the UL of the first bin succeeded, this row is fully masked. `np.unique` collapses the masked entries into one, so the uniqueness check in `MapAxis.__init__` fails with a misleading message.

**To Reproduce**
One needs to make the confidence failure deterministic. This can be done by replacing `Fit.confidence`
where failure is forced in e.g. the second energy bin.

```python
import astropy.units as u
from gammapy.datasets import SpectrumDataset
from gammapy.estimators import FluxPointsEstimator
from gammapy.maps import MapAxis, RegionGeom
from gammapy.modeling import Fit
from gammapy.modeling.models import PowerLawSpectralModel, SkyModel

energy = MapAxis.from_energy_bounds("1 TeV", "10 TeV", nbin=6)
energy_true = MapAxis.from_energy_bounds("0.5 TeV", "20 TeV", nbin=12, name="energy_true")
geom = RegionGeom.create("icrs;circle(83.63, 22.01, 0.1)", axes=[energy])

dataset = SpectrumDataset.create(geom=geom, energy_axis_true=energy_true, name="d")
dataset.exposure.quantity = 1e10 * u.Unit("m2 s")
dataset.background.data += 10.0
dataset.mask_safe.data[...] = True
dataset.models = SkyModel(PowerLawSpectralModel(), name="src")
dataset.fake(random_state=0)

# Force an invalid UL in the second energy bin only
_confidence = Fit.confidence
calls = {"n": 0}

def confidence(self, *args, **kwargs):
    calls["n"] += 1
    result = _confidence(self, *args, **kwargs)
    if calls["n"] == 2:
        result["success"] = False  # -> norm_ul = NaN -> fallback scan
    return result

Fit.confidence = confidence

FluxPointsEstimator(
    energy_edges=[1, 2, 5, 10] * u.TeV,
    source="src",
    selection_optional=["ul"],
    n_jobs=1,
).run(datasets=[dataset])
# ValueError: MapAxis: node values must be unique
```


**Other information**
Any other information you think will be useful for us to fix the issue can go here.

