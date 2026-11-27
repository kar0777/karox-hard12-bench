You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Allow editing cell geometry definition

## Is your feature request related to a problem? Please describe.

I recently needed to swap out the `pz` surfaces of a box, and was rather frustrated by the process. I ended up doing:

``` python
cell = montepy.Cell("1 0 -2 3 -4 5 -6 7 imp:n=1")
...
new_geom = None
for surf in cell.surfaces:
    if surf.surface_type not in {montepy.SurfaceType.PX, montepy.SurfaceType.PY}:
       continue
    if surf.location < 0:
        side = -surf
    else:
        side = +surf
    if new_geom is None:   
        new_geom = side
    else:
       new_geom &= side
new_geom &= -new_top & +new_bot
cell.geometry = new_geom
```


## Describe the solution you'd like

I would like an easier way to instead edit this geometry. I'm not sure exactly what this should look like yet. Here are a few thoughts though:

* Add a `def replace(replacer: tuple[Surface]):` that does a surface for surface replacement in a more user friendly way.
* Introduce an easy way to traverse the geometry tree, and to delete nodes
* Add a `delete_surface` function. This may need to have some restrictions to ensure logic is consistent. Such as only working when all one operator is used. 
* Make an easy way to traverse a tree and get the operators, side, and surface so it's easy to rebuild the geometry from scratch. 

## Describe alternatives you've considered

Just force users to redefine geometries from scratch. 

