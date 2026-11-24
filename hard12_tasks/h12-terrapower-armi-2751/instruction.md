You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

stdout falsely reports that a material has both material modifications and custom isotopics

I have a model that, when run, reports the following in the stdout:
```
[warn] Custom isotopics and material modifications have both been defined for Custom for component<Hexagon: homogeneous component>. Please consider carefully if these are in conflict.
[warn] Custom isotopics and material modifications have both been defined for Custom for component<Hexagon: sodium>. Please consider carefully if these are in conflict.
```

My blueprints do not contain any material modifications, so this error appears to be incorrect.

I cannot attach the inputs to this ticket, but will send them to you offline @john-science .
