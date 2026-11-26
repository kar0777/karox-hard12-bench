You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Fix `UxDataset.integrate()` to work for multiple data arrays in the dataset

**Describe the feature you'd like added to this project**

This method currently works only if there is a single data array in the dataset. 

A deprecation warning has started to be shown after PR #460. In the November release (v2023.11.0), replace it with a version that can work with multiple data arrays in a dataset.

**Describe the solution you'd like**
For integration of multiple data arrays in the dataset, use the `UxDataArray.integrate()` method for each of them and return a new dataset with the integrated values. 

