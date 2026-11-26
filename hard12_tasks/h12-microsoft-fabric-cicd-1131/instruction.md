You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[QUESTION] Environment variable replacement requires `$ENV:` in the actual OS variable name

### What is the question?

The `enable_environment_variable_replacement` feature flag is meant to let users reference environment variables in `parameter.yml` using a `$ENV:VAR_NAME` token.

However, the current implementation appears to require the actual OS environment variable to be named with the `$ENV:` prefix. This seems impractical: AFAIK, no shell or CI system will allow a variable name that starts with `$ENV:`. So, it's effectively unusable outside of manually poking `os.environ` in a Python wrapper.

Would it be better to keep the plain OS variable name (`VAR_NAME`) and use `$ENV:` only as the in-file token prefix? Or am I missing something?

### Context

We currently run fabric-cicd via the fabric-cli command `fab deploy`, so we can only use real OS environment variables—we cannot set keys on `os.environ` from a Python wrapper.

### Library Version

_No response_

### Operating System

Not applicable

### Have you checked the documentation?

- [x] I have searched existing GitHub issues
- [x] I have reviewed the fabric-cicd documentation

### Additional Information

_No response_
