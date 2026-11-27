You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Make pre-installed Python environments accessible during build

### Summary

A simple fix could be to add `--system-site-packages` to `python -m venv`, but I'm not sure what kind of unintended side effects this has.

### Why is this needed?

This is for example important when users build their own base image with some packages built from source, or when using a Pytorch base image. Without this feature, the pre-configured environments are not used.

### Usage example

n/a
