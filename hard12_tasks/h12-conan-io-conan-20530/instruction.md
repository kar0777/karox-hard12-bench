You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[feature] Support excluding the consumer from *@ settings patterns

### What is your suggestion?

A common setup builds every third-party dependency in Release while the user's own code follows the requested `build_type`. Debug builds of a large dependency graph then stay fast, binary-cache hits go up, and only the code you're actually debugging is built in Debug.

We'd like:
  - every dependency without user/channel (for example ConanCenter recipes, which have no user/channel) in Release, including new ones added to the graph later
  - our own packages (with a user/channel, e.g. `@company/stable`) to follow the requested `build_type`
  - the consumer (a local `conanfile.py`, `--requires`, the package of `conan create` and its test_package) to follow the requested `build_type`

### Have you read the CONTRIBUTING guide?

- [ ] I've read the CONTRIBUTING guide
