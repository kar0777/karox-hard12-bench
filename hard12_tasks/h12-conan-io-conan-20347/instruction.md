You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[bug] CMakeConfigDeps silently drops cpp_info.components[...].objects

### Describe the bug

We currently use CMakeDeps and I was trying out CMakeConfigDeps with conan 2.32.0.

We have an internal recipe that exposes a precompiled object file via self.cpp_info.components["objects"].objects = ["/path/to/lib/foo.o"]. It works correctly with CMakeDeps (produces an IMPORTED_OBJECTS  property on the imported target, and the .o ends up in the final link command of any consumer).

With CMakeConfigDeps, the same recipe produces a CMake target for the objects component, but it is an empty INTERFACE IMPORTED library and IMPORTED_OBJECTS  is never set. This is the relevant part in the foo-Targets-debug.cmake file generated.

```
#################### foo::objects ####################
if(NOT TARGET foo::objects)
    message(STATUS "Conan: Target declared imported INTERFACE library 'foo::objects'")
    add_library(foo::objects INTERFACE IMPORTED)
endif()

set_property(TARGET foo::objects APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
```

Took me a while to figure out because the .o file is silently dropped from every consumer's link line without an error or warning.

Is this intended to be supported at some point? Thanks!

### How to reproduce it

_No response_
