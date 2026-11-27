You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[feature] Expose replace_requires to command line. Allow ignoring replace_require.

### What is your suggestion?

When developing packages locally, we need a way to override / ignore / change `replace_requires` in regards to our currently developed package. If not, local changes are ignored by conan create which pulls the recipe from upstream. Our profiles contain so many settings and options we cannot build without them.

I'm sure there are other moments you'd want to change, remove, test different versions in command line.

There's an argument to be made a replace require may *always* want to be ignored for the currently created package. But that may have ramifications or consequences I haven't taken the time to think about.

ex
```bash
# Some way to ignore all replace requires.
conan create ... --ignore-replace-requires

# Some way to ignore a specific package(s) replace requires.
conan create ... --ignore-replace-requires my_package/*

# Some way to change the replace require completely.
conan create . --version 42 --user potato --channel tomato --replace-requires my_package/*@*/*:my_package/42@potato/tomato

# maybe?
# Becomes : my_package/*:my_package/42@potato/tomato
conan create . --version 42 --user potato --channel tomato --replace-requires my_package/*:my_package/*@*/*
```

### Have you read the CONTRIBUTING guide?

- [x] I've read the CONTRIBUTING guide
