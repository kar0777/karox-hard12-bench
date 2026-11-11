You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Extend LambdaAttributeAssignedViolation rule

Should `LambdaAttributeAssignedViolation` ([link](https://github.com/wemake-services/wemake-python-styleguide/blob/master/wemake_python_styleguide/violations/oop.py#L675)) also detect lambda values assigned through unpacked assignments, not only direct `self.attr = lambda ...` assignments?

I found this [TODO](https://github.com/wemake-services/wemake-python-styleguide/blob/master/tests/test_visitors/test_ast/test_classes/test_lambda_attr_assign.py#L40). Is still relevant? Can I work on it?
