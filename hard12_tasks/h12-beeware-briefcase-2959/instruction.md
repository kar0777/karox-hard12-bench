You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

"Mark of the Web" prevents Windows app from running when distributed as a ZIP file

### Describe the bug

When a ZIP-packaged app is extracted and runs, a stacktrace is shown when loading DLLs fails (as seen in https://github.com/beeware/briefcase/discussions/1881).

This first happens when pythonnet tries to load its Python runtime DLL (Python.Runtime.dll) and then for the WebView DLL from toga-winforms.

The underlying issue is Windows' [Mark of the Web](https://learn.microsoft.com/en-us/deployoffice/security/internet-macros-blocked#additional-information-about-mark-of-the-web) (MotW) functionality that prevents running foreign code while the file is marked.

### Steps to reproduce

Package an app for Windows using ZIP. Extract and run that app on another machine.

### Expected behavior

The app should successfully run.

The issue can be worked around by manually removing the MotW from all DLLs in the app (via selecting "Unblock" in the DLL file's properties).

To bypass the MotW check automatically, we can tell the .NET runtime to [allow loading](https://learn.microsoft.com/en-us/previous-versions/dotnet/netframework-4.0/dd409252(v=vs.100)) remote sources.

This can be accomplished via a `<App Formal Name>.exe.config` file alongside the app's stub exe:
```xml
<configuration>
   <runtime>
      <loadFromRemoteSources enabled="true"/>
   </runtime>
</configuration>
```

Since this is not needed for MSI packages, it may be best to add this file only when packaging as a ZIP.

### Screenshots

_No response_

### Environment

- Operating System: Windows 11
- Python version: 3.11
- Software versions:
  - Briefcase: `0.3.20.dev15+g93ee7e9f`


### Logs

```
  File "\app_packages\toga_winforms\__init__.py", line 1, in <module>
    import clr
  File "\app_packages\clr.py", line 6, in <module>
    load()
  File "\app_packages\pythonnet\__init__.py", line 143, in load
    func = assembly.get_function("Python.Runtime.Loader.Initialize")
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "\app_packages\clr_loader\types.py", line 94, in get_function
    return ClrFunction(self._runtime, self._path, name, func)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "\app_packages\clr_loader\types.py", line 58, in __init__
    self._callable = runtime._get_callable(assembly, typename, func_name)
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "\app_packages\clr_loader\netfx.py", line 47, in _get_callable
    raise RuntimeError(
RuntimeError: Failed to resolve Python.Runtime.Loader.Initialize from \app_packages\pythonnet\runtime\Python.Runtime.dll
```
### Additional context

_No response_
