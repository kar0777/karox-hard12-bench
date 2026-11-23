You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[bug] Windows environment variables intermittently stripped during recipe execution

### Description

When running Conan recipes on Windows, basic system environment variables (`ProgramData`, `SystemRoot`, `COMSPEC`, etc.) are **intermittently missing** during recipe method execution (`generate()`, `build()`). This causes `vswhere.exe` (used by CMake to discover Visual Studio) to fail with COM initialization error `0x80131904`, resulting in "could not find any instance of Visual Studio" errors.

The issue is non-deterministic: approximately 25% of identical runs fail while the rest succeed.
I faced the same behavior across multiple machines used in CI/CD pipelines.

### Expected behavior
All Windows system environment variables should be preserved/inherited during recipe execution. CMake should successfully discover Visual Studio on every run.

### Environment
Conan version: 2.24.0
Python version: 3.7.8
Operating System: Windows Server 2022 (windows/amd64)
CMake version: 3.31.6
Visual Studio: 2022 Enterprise (v17, toolset v143)
Installation method: pipx
CI Environment: GitLab Runner 18.2.2 (shell executor, Git Bash → Python/Conan)

### Output/Logs
#### Failing run (env vars missing):
```
mypkg/1.0: Calling build()
mypkg/1.0: ProgramData: MISSING
mypkg/1.0: SystemRoot: MISSING
mypkg/1.0: COMSPEC: MISSING
CMake Error at CMakeLists.txt:2 (project):  
    Generator    
        Visual Studio 17 2022  
    could not find any instance of Visual Studio.
-- Configuring incomplete, errors occurred!
```

#### Successful run (same code, same machine):
```
mypkg/1.0: Calling build()
mypkg/1.0: ProgramData: C:\ProgramData
mypkg/1.0: SystemRoot: C:\Windows
mypkg/1.0: COMSPEC: C:\Windows\system32\cmd.exe
-- Selecting Windows SDK version 10.0.19041.0 to target Windows 10.0.19045.
-- The CXX compiler identification is MSVC 19.43.34808.0
-- Build files have been written to: ...
```

### Additional context
1. ~25% failure rate, not deterministic
2. Not tied to specific machines - happens across multiple Windows runners
3. I use the same machines and recipes to create conan v1 package and it works fine.

Current workaround is to set the environment variables in the recipe.

### How to reproduce it

1. Create a simple conanfile using CMake with Visual Studio generator:

```python
class MyPackage(ConanFile):
    name = "mypkg"
    version = "1.0"
    settings = "os", "compiler", "build_type", "arch"
    exports_sources = "CMakeLists.txt", "*.cpp"
    
    def layout(self):
        cmake_layout(self)

    def generate(self):
        from conan.tools.cmake import CMakeToolchain
        CMakeToolchain(self).generate()
    
    def build(self):
        import os
        self.output.info(f"ProgramData: {os.environ.get('ProgramData', 'MISSING')}")
        self.output.info(f"SystemRoot: {os.environ.get('SystemRoot', 'MISSING')}")
        self.output.info(f"COMSPEC: {os.environ.get('COMSPEC', 'MISSING')}")
        
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
    
    def package(self):
        cmake = CMake(self)
        cmake.install()
```

2. Run the recipe
3. Observe that ~25% of runs fail with missing VS, while the diagnostic shows MISSING for env vars.
