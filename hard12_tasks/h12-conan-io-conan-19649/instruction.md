You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[feature] Have a way to generate both conanbuild.bat and conanbuild.ps1 files.

<!-- What is your suggestion? Please be as specific as possible! -->

It would be handy to have a way `tools.env.virtualenv:powershell` to create _both_ `.ps1` and `.bat` files. 

- `.ps1` to activate within a user's interactive PowerShell if necessary.
- `.bat` for when build scripting is using CMD to issue commands, and it needs to activate the environment to run CMake or some other command.

- [x] I've read the [CONTRIBUTING guide](https://github.com/conan-io/conan/blob/develop/.github/CONTRIBUTING.md).

This came out of using `conan.tools` to make a Conan 2.0-ish workflow while using Conan 1.

