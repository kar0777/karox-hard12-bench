You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[bug] CMakeConfigDeps renders self.cpp.build.component[...].location relative to package folder rather than build_folder

### Describe the bug

When consuming a recipe that is configured as an editable package, CMakeConfigDeps renders the `self.cpp.build.component[...].location` field relative to the package folder rather than the build folder.

```
# This is the result ATM:
set_target_properties(App::test PROPERTIES IMPORTED_LOCATION_RELEASE "${app_PACKAGE_FOLDER_RELEASE}/Release/test.exe")

# This is what it I suspect it should be
set_target_properties(App::test PROPERTIES IMPORTED_LOCATION_RELEASE "${app_PACKAGE_FOLDER_RELEASE}/build/Release/test.exe")
```

Also - it's not clear from the documentation what the `cpp_info.exe` field is meant to reference.  There's 2 usages of it in the conan center, and it would appear that it should *just* refer to the name of the executable (without path and extension??).

Similarly, the `cpp_info.location` documentation suggests that it should refer to the "full location (path and filename with extension) of the artifact".  The conan center usages actually explicitly prefix the location path with `self.package_folder` to make it an absolute (i.e. "full") path, but I suspect they should probably not be doing that.  It might suggest that the documentation could be refined to better describe the field (or I could be wrong with *my* assumption!)

I'm running Conan 2.29.0 on Windows.

### How to reproduce it

_No response_
