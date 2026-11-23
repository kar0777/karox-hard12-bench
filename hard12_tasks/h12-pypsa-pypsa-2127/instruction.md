You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

assigning `committable` to non-supporting components should raise on assignment


---

EDIT by @FabianHofmann : 

The root cause for the following issue it the non-fail-fast assignment of a `committable` attribute to component which do not allow for it.  I updated the title of the issue. 

*Original issue below*

---

### Version Checks (indicate both or one)

- [x] I have confirmed this bug exists on the lastest [release](https://github.com/pypsa/pypsa/releases) of PyPSA.

- [x] I have confirmed this bug exists on the current [`master`](https://github.com/pypsa/pypsa/tree/master) branch of PyPSA.


### Issue Description

When creating the model, the code crashes when there are storage-units present within the network only if set to True. From the create_model(), we are looping over the variable "Storage-units-p_dispatch" and "Storage-units-p_store". This results in adding the variable Storage-units_status twice causing the error. 

### Reproducible Example

```python
import logging
import os

import numpy as np
import pandas as pd
import pypsa

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def create_minimal_network(n_snapshots=24):
    """
    Create a minimal PyPSA network for testing rolling horizon dispatch.
    
    Parameters
    ----------
    n_snapshots : int
        Number of hourly snapshots to create
        
    Returns
    -------
    pypsa.Network
        A minimal network with generator, load, and storage unit
    """
    # Create network
    n = pypsa.Network()
    
    # Create snapshots (hourly for one day)
    snapshots = pd.date_range("2024-01-01", periods=n_snapshots, freq="h")
    n.set_snapshots(snapshots)
    
    # Add buses
    n.add("Bus", "bus_0", v_nom=1.0)
    n.add("Bus", "bus_1", v_nom=1.0)
    
    # Add carrier
    n.add("Carrier", "gas", co2_emissions=0.2)
    n.add("Carrier", "battery", co2_emissions=0.0)
    
    # Add a gas generator - dispatchable
    n.add(
        "Generator",
        "gas_gen",
        bus="bus_0",
        carrier="gas",
        p_nom=100,  # MW
        marginal_cost=50,  # $/MWh
        committable=True,
        min_up_time=2,
        min_down_time=2,
        up_time_before=0,
        down_time_before=4,
    )
    
    n.add(
        "StorageUnit",
        "battery",
        bus="bus_0",
        carrier="battery",
        p_nom=50,  # MW charging/discharging capacity
        max_hours=4,  # 4-hour battery (50 MW * 4h = 200 MWh)
        efficiency_store=0.95,
        efficiency_dispatch=0.95,
        marginal_cost=1,  # Small cost to prefer generator over battery
        state_of_charge_initial=50,  # Start at 50 MWh
        committable=True,  # Set to False to avoid PyPSA bug with status variables
    )
    
    # Add load with varying demand (sinusoidal pattern)
    hours = range(n_snapshots)
    base_load = 60  # MW
    load_variation = 20  # MW
    load_profile = [
        base_load + load_variation * (0.5 + 0.5 * np.sin(2 * np.pi * h / 24))
        for h in hours
    ]
    
    n.add("Load", "load", bus="bus_0", p_set=0)
    n.loads_t.p_set["load"] = load_profile
    
    # Add link between buses
    n.add(
        "Link",
        "link_0_1",
        bus0="bus_0",
        bus1="bus_1",
        p_nom=75,  # MW
        efficiency=0.98,
    )
    
    return n



def main():
    """Main execution function."""
    logger.info("Creating minimal network...")
    network = create_minimal_network(n_snapshots=24)
    
    logger.info("\nNetwork summary:")
    logger.info(f"Generators:\n{network.generators[['bus', 'carrier', 'p_nom', 'committable', 'marginal_cost']]}")
    logger.info(f"\nStorage Units:\n{network.storage_units[['bus', 'carrier', 'p_nom', 'max_hours', 'committable']]}")
    logger.info(f"\nLoads:\n{network.loads[['bus', 'p_set']]}")
    
    # Run rolling horizon optimization
    logger.info("\n" + "="*60)
    logger.info("Starting rolling horizon dispatch simulation")
    logger.info("="*60)
    
    network.optimize.optimize_with_rolling_horizon(
        snapshots=network.snapshots,
        horizon=6,  # 6-hour optimization periods
        overlap=0,  # No overlap in simplified version
        solver_name="highs",
        linearized_unit_commitment=False,
    )


if __name__ == "__main__":
    main()
```

### Expected Behavior

Traceback (most recent call last):
  File "C:\Users\mbui\Desktop\github\alignment_error\storage-units-committable.py", line 127, in <module>
    main()
  File "C:\Users\mbui\Desktop\github\alignment_error\storage-units-committable.py", line 117, in main
    network.optimize.optimize_with_rolling_horizon(
  File "C:\Users\mbui\Desktop\github\PyPSA\pypsa\optimization\abstract.py", line 543, in optimize_with_rolling_horizon
    status, condition = n.optimize(sns, **kwargs)
                        ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\mbui\Desktop\github\PyPSA\pypsa\optimization\optimize.py", line 562, in __call__
    m = n.optimize.create_model(
        ^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\mbui\Desktop\github\PyPSA\pypsa\optimization\optimize.py", line 679, in create_model
    define_status_variables(n, sns, c, linearized_unit_commitment)
  File "C:\Users\mbui\Desktop\github\PyPSA\pypsa\optimization\variables.py", line 90, in define_status_variables
    n.model.add_variables(
  File "C:\Users\mbui\.venv\pypsa_github\Lib\site-packages\linopy\model.py", line 531, in add_variables
    raise ValueError(f"Variable '{name}' already assigned to model")
ValueError: Variable 'StorageUnit-status' already assigned to model

### Installed Versions

<details>
Windows - Python 3.12
Bottleneck==1.6.0
certifi==2026.2.25
cffi==2.0.0
cftime==1.6.5
charset-normalizer==3.4.4
click==8.3.1
cloudpickle==3.1.2
colorama==0.4.6
contourpy==1.3.3
cryptography==46.0.5
cycler==0.12.1
dask==2026.1.2
deprecation==2.1.0
fonttools==4.61.1
fsspec==2026.2.0
geopandas==1.1.2
google-api-core==2.30.0
google-auth==2.48.0
google-cloud-core==2.5.0
google-cloud-storage==3.9.0
google-crc32c==1.8.0
google-resumable-media==2.8.0
googleapis-common-protos==1.72.0
highspy==1.13.1
idna==3.11
Jinja2==3.1.6
kiwisolver==1.4.9
Levenshtein==0.27.3
linopy==0.6.4
locket==1.0.0
MarkupSafe==3.0.3
matplotlib==3.10.8
narwhals==2.17.0
netCDF4==1.7.3
networkx==3.6.1
numexpr==2.14.1
numpy==2.4.2
packaging==26.0
pandas==3.0.1
partd==1.4.2
pillow==12.1.1
plotly==6.5.2
polars==1.38.1
polars-runtime-32==1.38.1
proto-plus==1.27.1
protobuf==6.33.5
pyasn1==0.6.2
pyasn1_modules==0.4.2
pycparser==3.0
pydeck==0.9.1
pyogrio==0.12.1
pyparsing==3.3.2
pyproj==3.7.2
-e git+https://github.com/PyPSA/PyPSA.git@2e22ebd6bd8315a5e6c51f7581cbb56aa7f1e4af#egg=pypsa
python-dateutil==2.9.0.post0
PyYAML==6.0.3
RapidFuzz==3.14.3
requests==2.32.5
rsa==4.9.1
scipy==1.17.1
seaborn==0.13.2
shapely==2.1.2
six==1.17.0
toolz==1.1.0
tqdm==4.67.3
tzdata==2025.3
urllib3==2.6.3
validators==0.35.0
xarray==2026.2.0
</details>

