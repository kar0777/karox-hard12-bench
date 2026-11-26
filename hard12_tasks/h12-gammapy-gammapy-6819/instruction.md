You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Check JFactory line-of-sight integration branch decomposition

**Gammapy version**
2.1

**Bug description**


In the current implementation, the radial integration domain is decomposed as

```text
2 × [b, D] + [D, 4D],
```
where `D` is the observer-to-halo distance and `b = D sin(theta)` is the impact parameter.

This radial branch decomposition is valid when the closest-approach point lies in front of the observer, i.e. for `theta < pi / 2`. In that case, the forward line of sight crosses radii between `D` and `b`, and then goes back from `b` to larger radii. Therefore, the radial interval `[b, D]` corresponds to two line-of-sight branches.

  But for `theta >= pi / 2`, the closest-approach point lies behind the observer. Along the physical forward line of sight, the radius then increases from `D` outward. So the radial interval `[b, D]` does not correspond to two forward line-of-sight branches anymore, and should not be counted with the same factor of two.

**Expected behavior**

The radial branch decomposition should depend on the angular separation.

For `theta < pi / 2`, the closest-approach point is in front of the observer, so the radial mapping of the forward line of sight contains two branches over `[b, D]`, followed by the outer branch beyond `D`.

For `theta >= pi / 2`, the closest-approach point is behind the observer. Along the forward line of sight, the radius starts at `D` and increases outward, so the doubled `[b, D]` radial contribution should not be included.

**To Reproduce**

The issue can be seen from the line-of-sight geometry. For an observer at distance `D` from the halo center and angular separation `theta`, the radius along the line of sight is

```text
r(l)^2 = D^2 + l^2 - 2 D l cos(theta),
```
where `l >= 0` is the physical forward line-of-sight coordinate.

The closest-approach point occurs at

```text
l_closest = D cos(theta).
```

For `theta > pi / 2`, `l_closest` is negative, meaning that the closest approach is behind the observer.

Minimal geometry check:

```python
import numpy as np
from gammapy.astro.darkmatter import profiles

distance = profiles.DMProfile.DISTANCE_GC

for theta_deg in [30, 90, 120]:
    theta = np.deg2rad(theta_deg)
    impact = distance * np.sin(theta)
    l_closest = distance * np.cos(theta)

    print(f"theta = {theta_deg} deg")
    print(f"  impact = {impact:.3g}")
    print(f"  l_closest = {l_closest:.3g}")
```

For `theta = 120 deg`, `l_closest` is negative. This shows that the closest-approach point is not on the physical forward line of sight, even though it still appears as the lower bound of the radial parametrization.

**Other information**

This issue is intended as a follow-up to PRs #6743 and #6757. 
