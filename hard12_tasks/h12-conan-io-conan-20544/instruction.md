You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[question] Recommended approach for warning-as-error missing files in virtual package

### What is your question?

We are successfully building with `core:warnings_as_errors=['*']` for almost everything. We use some virtual packages in the same manner as the [c-c-i opengl virtual package](https://github.com/conan-io/conan-center-index/blob/master/recipes/opengl/all/conanfile.py).

When building opengl or our other virtual packages, we still get the warning promoted to an error of "No files in this package!". What is the recommended approach to be able to address this warning for virtual packages. The idea of creating a dummy file just to silence the warning is a workable kludge but doesn't seem particularly clean.

### Have you read the CONTRIBUTING guide?

- [x] I've read the CONTRIBUTING guide
