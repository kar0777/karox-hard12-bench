You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Material.getProperty not correctly passing Temps in Celcius to matProps

ARMI's `Material.getProperty()` takes in temperature in Celsius or Kelvin:

https://github.com/terrapower/armi/blob/ce01b794b0f128303adcf6faf072cc1e89e34c59/armi/materials/material.py#L517

And does the same thing all the other `Material` property functions do, which is convert things to Kelvin immediately:

https://github.com/terrapower/armi/blob/ce01b794b0f128303adcf6faf072cc1e89e34c59/armi/materials/material.py#L525

But there is an edge case where the material is called directly from `matProps`, and thus should be:

1. Converted to Celcius
2. Called `T`, because `matProps` doesn't care about other units.

This:

https://github.com/terrapower/armi/blob/ce01b794b0f128303adcf6faf072cc1e89e34c59/armi/materials/material.py#L533-L535

should become this:

```python
            Tc = getTk(Tc, Tk)
            val = getattr(self, propName)(T=Tc, **kwargs)
            # cache only one value for each property. Prevents unbounded cache explosion.
            self._setCache(propName, (Tk, val))
```
