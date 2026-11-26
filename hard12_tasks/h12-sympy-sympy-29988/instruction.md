You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

integrate x**2*exp(-x**2)*ln(x)

```python
In [12]: manualintegrate(x**2*exp(-x**2)*ln(x), x)
Out[12]: 
⌠                  
⎮       2          
⎮  2  -x           
⎮ x ⋅ℯ   ⋅log(x) dx
⌡                  

In [13]: integrate(x**2*exp(-x**2)*ln(x), x)
Out[13]: 
⌠                  
⎮       2          
⎮  2  -x           
⎮ x ⋅ℯ   ⋅log(x) dx
⌡                  

In [14]: 
```

<img width="1037" height="265" alt="Image" src="https://github.com/user-attachments/assets/42cc9dc6-742f-4cb8-90bd-d30219bc25dc" />
