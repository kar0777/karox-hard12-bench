You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Add `.nrefs` method to accessor that returns number of virtual chunk references

It would be neat to add a method `vds.nrefs()` to the accessor, which returns the total number of virtual references in the dataset. It's useful to know how many millions of references you're about to try and write to icechunk (or kerchunk json...)

```python
class VirtualDatasetAccessor
    def nrefs(self: xr.Dataset) -> int:
        """Count the number of virtual references in the dataset"""
        from virtualizarr.manifests import ManifestArray
    
        # this just ignores non-virtual variables
        return sum(
            len(var.data.manifest) for var in vds.variables.values() if isinstance(var.data, ManifestArray)
        )
```
