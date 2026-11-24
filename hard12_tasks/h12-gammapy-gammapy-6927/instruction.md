You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

EventList.peek(): x-axis labels overlap on Energy [TeV] panels

The x-axis tick labels on the "Energy [TeV]" panels are overlapping and hard to read.

**Code:**
```python
import astropy.units as u
from gammapy.data import EventList
filename = '$GAMMAPY_DATA/hess-dl3-dr1/data/hess_dl3_dr1_obs_id_023523.fits.gz'
events = EventList.read(filename)

# Select events based on energy
selected_energy = events.select_energy([1*u.TeV, 1.2*u.TeV])
selected_energy.peek()
```

**Expected:** labels should not overlap — maybe rotate them or show fewer ticks.

**Gammapy version:** 2.1

<img width="1081" height="677" alt="Image" src="https://github.com/user-attachments/assets/4684c535-6cc6-4235-9fcd-3fb4db766be0" />
