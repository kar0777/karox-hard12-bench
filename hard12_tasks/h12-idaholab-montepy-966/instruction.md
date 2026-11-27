You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

MontePy does not print enough significant figures in generated surface definitions

## Is your feature request related to a problem? Please describe.

I'm always frustrated when...

...generating surfaces and losing precision when the meaningful change in numbers is beyond the 5th significant digit.


## Bug Description

MontePy strives to maintain formatting consistency when modifying existing inputs. When generating new inputs, it makes some assumptions. One of the assumptions appears to be 5 significant figures.

This can lead to loss of accuracy when working with numbers where the meaning


## To Reproduce

<!-- A short code snippet of what you have ran. Please change or remove any specific values or anything that can't be public. For example: --> 

``` python
import montepy

surf1 = montepy.SphereAtOrigin()
surf1.number = 1
surf1.radius = 100.01

surf2 = montepy.SphereAtOrigin()
surf2.number = 2
surf2.radius = surf1.radius + 1e-4

surf3 = montepy.SphereAtOrigin()
surf3.number = 3
surf3.radius = 1 + 1e-4

print(surf1.mcnp_str())
print(surf2.mcnp_str())
print(surf3.mcnp_str())
```

## Output

<details open> 

``` 
1 SO 100.01 
2 SO 100.01 
3 SO 1.0001 
```

## Workaround

```python
montepy.input_parser.syntax_node.ValueNode._FORMATTERS[float]["precision"] = 16
```

```
1 SO 100.01 
2 SO 100.0101 
3 SO 1.0001
```

</details>

## Describe the solution you'd like

<!-- A clear and concise description of what you want to happen. -->

Expose float precision formatting to the user in a transparent way.


## Additional context

Could be a setting handled through e.g. #103 

