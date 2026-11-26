You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[feature] Support CMake arbitrary preset files

### What is your suggestion?

Currently, Conan's CMakeToolchain generator relies on generating a `CMakeUserPresets.json` file in the source directory, which prohibits using this generator while trying to maintain a read-only source tree. 

Failing to maintain a read-only source tree means the source tree cannot be used for multiple builds at once, which makes doing development and validation for different build flavors, variants, or platforms simultaneously very difficult.

Fortunately, in [CMake 4.4](https://cmake.org/cmake/help/latest/release/4.4.html), a new `--presets-file` argument has been added, which means Conan no longer needs to write to the source directory to supply the presets functionality that it does today.

Conan should support a feature to change preset file generation to instead create a `ConanCMakePresets.json` file in the relevant directory (build/output/generators/etc). Conan's [documentation on using CMake presets](https://docs.conan.io/2/examples/tools/cmake/cmake_toolchain/build_project_cmake_presets.html) should be updated to reflect this new workflow.

The original behavior of writing `CMakeUserPresets.json` to the source tree should be deprecated, ideally moving to a model where the default for new projects is to only use the output-folder presets file. I don't know much about Conan's deprecation policies/mechanisms and lifespans so I can't comment on how exactly that should be done.

### Have you read the CONTRIBUTING guide?

- [x] I've read the CONTRIBUTING guide
