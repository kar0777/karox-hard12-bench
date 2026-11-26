You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Density of a custom material is zero despite knowing the density

Related to #1682: `Material.density` returns zero, probably under the assumption a subclass will override the method. And most cases that's true.

But, if you make a custom material in the blueprint file and provide a mass density, the `CustomMaterial` object does not override the density and will return zero. This is despite the fact that is known by the class

https://github.com/terrapower/armi/blob/7b26f79ac8c58b0477b0d7fa384b363d10fa9406/armi/materials/custom.py#L40

and used in the `pseudoDensity` method

https://github.com/terrapower/armi/blob/7b26f79ac8c58b0477b0d7fa384b363d10fa9406/armi/materials/custom.py#L42-L50

But, if you have a routine that does something with a subclass of `Material` and relies on `Material.density`, you can see strange problems because `CustomMaterial.density` falls back to `Material.density` which relies on the `refDens` property

https://github.com/terrapower/armi/blob/7b26f79ac8c58b0477b0d7fa384b363d10fa9406/armi/materials/material.py#L492-L514

which defaults to zero

https://github.com/terrapower/armi/blob/7b26f79ac8c58b0477b0d7fa384b363d10fa9406/armi/materials/material.py#L101
