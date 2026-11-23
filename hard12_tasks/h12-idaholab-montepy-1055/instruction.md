You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Geometry is not kept in sync with its cell and problem

## Bug Description

A cell's geometry tree isn't kept in sync with the cell and its problem. `read_input` links every node to the cell through `HalfSpace._cell`, by way of `update_pointers`, but the other routes don't:

| Route | Nodes linked |
|---|---|
| `read_input` | All |
| `cell.geometry = ...` | Root only |
| `HalfSpace.left = ...` or `.right = ...` | None of the new nodes |
| `montepy.Cell("...")` | None |
| `cell.clone()` | Linked to a deep copy of the original cell, not to the clone |

`HalfSpace.replace` and the `UnitHalfSpace.divider` setter use the link to keep `Cell.surfaces` and `Cell.complements` up to date. This causes:

1. After `cell.geometry = ...`, `replace` on a tree with more than one leaf doesn't update `cell.surfaces`. If the cell is then appended to a problem, the old surface reaches `problem.surfaces` and the new one doesn't. Writing that problem gives an input that references an undefined surface, and reading it back raises `BrokenObjectLinkError`.
2. `replace` on a clone can raise `KeyError`.
3. Reassigning `cell.geometry` leaves the old surfaces and complements on the cell.
4. Changing the geometry of a cell that is already in a problem doesn't add new surfaces to the problem, through `replace`, `cell.geometry = ...`, or `&=`.
5. Setting `left` or `right` doesn't update the cell at all.

Found while working on #1033, where `HalfSpace.mcnp_str` looks up the version of the problem through this link.

## To Reproduce

``` python
import montepy


def plane(number):
    return montepy.AxisPlane(f"{number} PZ {float(number)}")


# 1. the setter only links the root
s1, s2, s3 = plane(1), plane(2), plane(3)
cell = montepy.Cell(number=1)
cell.geometry = -s1 & +s2
cell.geometry.replace(s1, s3)
problem = montepy.MCNP_Problem("foo")
problem.cells.append(cell)
print(cell.geometry)                         # (-3*+2)
print([s.number for s in cell.surfaces])     # [1, 2], expected [2, 3]
print([s.number for s in problem.surfaces])  # [1, 2], expected [2, 3]

# 2. clones are linked to a copy of the original cell
s1, s3 = plane(1), plane(3)
cell = montepy.Cell(number=1)
cell.geometry = -s1
clone = cell.clone()
print(clone.geometry._cell is clone)  # False
clone.geometry.replace(list(clone.surfaces)[0], s3)  # KeyError

# 3. reassigning leaves the old surfaces behind
s1, s2 = plane(1), plane(2)
cell = montepy.Cell(number=1)
cell.geometry = -s1
cell.geometry = -s2
print([s.number for s in cell.surfaces])  # [1, 2], expected [2]

# 4. parsed cells are not linked
cell = montepy.Cell("1 0 -1 imp:n=1")
print(cell.geometry._cell)  # None
```

## Error Message

Only case 2 raises at the time of the change:

<details open>

``` python
Traceback (most recent call last):
  File "example.py", line 10, in <module>
    clone.geometry.replace(list(clone.surfaces)[0], s3)
  File "montepy/surfaces/half_space.py", line 315, in replace
    container.remove(old_divider)
  File "montepy/numbered_object_collection.py", line 406, in remove
    raise KeyError(f"This object is not in this collection")
KeyError: 'This object is not in this collection'
```

</details>

## MCNP input file snippet

No input file is needed.

## Version

 - `1.5.1.dev104+gafa420935`, also reproduced on `1.5.0`

## Additional context

The setter can't be used from `_parse_geometry`, because it raises `IllegalState` on dividers that are still numbers, so the link needs a step that doesn't resolve them.

One related case is not covered by the fix I'm opening: setting `UnitHalfSpace.divider` directly doesn't remove the old divider from the cell or add the new one to the problem. `remove_duplicate_surfaces` goes through that setter, including during `Cell.clone`, so changing it needs more care. `HalfSpace.replace` is the route that handles both.

