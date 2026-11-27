You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Incorrect behaviour of sum_over_energy_groups in class Estimator

**Gammapy version**
2.1 (and dev)

**Expected behavior / Bug description**
In gammapy.estimators.ExcessMapEstimator the following descriptions are given for 2 parameters : 

energy_edges :  Edges of the target maps energy bins. The resulting bin edges won’t be exactly equal to the input ones, but rather the closest values to the energy axis edges of the parent dataset. **Default is None: apply the estimator in each energy bin of the parent dataset**

sum_over_energy_groups : Only used if energy_edges is None. **If False, apply the estimator in each energy bin of the parent dataset.** If True, apply the estimator in only one bin defined by the energy edges of the parent dataset. 

From this I expect that not providing energy_edges and leaving sum_over_energy_groups to False would output an excess map per energy bin of the original dataset. Instead, independently of sum_over_energy_groups beeing True or False, a single energy bin is outputed. 


**To Reproduce**
Apply an ExcessMapEstimator to a dataset with multiple energy bins.

**Other information**
Looking in the source code of the class Estimator, I found this function : 
```    
def _get_energy_axis(self, dataset):
        """Energy axis."""
        if self.energy_edges is None:
            energy_axis = dataset.counts.geom.axes["energy"].squash()
            if getattr(self, "sum_over_energy_groups", False):
                energy_edges = [energy_axis.edges[0], energy_axis.edges[1]]
                energy_axis = MapAxis.from_energy_edges(energy_edges)
        else:
            energy_axis = MapAxis.from_energy_edges(self.energy_edges)

        return energy_axis
```
The squash on the energy axis means that only one energy bin is used, which I would expect to occur only if sum_over_energy_groups is True. Then, the `if getattr(self, "sum_over_energy_groups", False):` creates an energy axis from the first and second edges of the squashed energy axis. So it creates an identical single bin axis. Also, if there were more bins I would assume that the correct edges to take would be the first and the last, not the first and second.
