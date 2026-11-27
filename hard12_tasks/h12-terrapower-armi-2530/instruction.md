You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Is the class1/2_custom_isotopics Material logic unused?

@opotowsky and I have reason to believe the `class1_custom_isotopics` and `class2_custom_isotopics` logic in `Material.applyInputParams()` is unused:

https://github.com/terrapower/armi/blob/9a8a49c6e9d589b0a57e921ecd57a57e1a722a8a/armi/materials/material.py#L692-L694

https://github.com/terrapower/armi/blob/9a8a49c6e9d589b0a57e921ecd57a57e1a722a8a/armi/materials/material.py#L185-L188

We need to do a little research here. But this `classN_custom_isotopics` logic kind of gums up the works in the `Material` class, and I think it could be a LOT simpler.
