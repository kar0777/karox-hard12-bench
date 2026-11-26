You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[Console] - Misleading warnings when adding a catalog with aqua add

## Description:

When adding a catalog in editable mode on a fresh installation (empty ~/.aqua/catalogs), the command prints two warnings right after the catalog is installed:

```
$ aqua add obs -e ~/Climate-DT-catalog/catalogs/obs
Adding the AQUA catalog obs
Installing catalog in editable mode from .../Climate-DT-catalog/catalogs/obs to ~/.aqua
ConfigCatalog :: WARNING  -> No available catalogs found
ShowCatalog :: WARNING  -> No catalogs available to scan
```

The catalog is correctly installed (aqua list shows it), but the warnings suggest something went wrong, which can be confusing for new users.
