You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

libgssapi_krb5.so.2 cannot be found when importing PySide6.QtWebEngineWidgets under Flatpak

### Describe the bug

Even though you're using the PySide6-supporting base image, if you use QtWebEngineWidgets, it relies on a library, libgssapi_krb5.so.2, which cannot be found.

This results in

```
libgssapi_krb5.so.2: cannot open shared object file: No such file or directory
```

### Steps to reproduce

1. 
Build a standard PySide6 app. Make sure the runtime looks like

```
[tool.briefcase.app.my-app.linux.flatpak]                                                                                                                                                    
flatpak_runtime = "org.kde.Platform"                                                                                                                                                                
flatpak_runtime_version = "6.7"                                                                                                                                                                     
flatpak_sdk = "org.kde.Sdk"  
```


2.
Within the app, arrange to call:
 
```
from PySide6.QtWebEngineWidgets import QWebEngineView
```

3. 💥 



### Expected behavior

Because the library was imported, we expect this should successfully work.

### Screenshots

_No response_

### Environment

- Operating System: Linux, Ubuntu 24.04 LTS
- Python version: 3.12
- Software versions:
  - Briefcase: 0.3.22

### Logs

```

```


### Additional context

## Workaround

You can work around this by building `mit-krb5` from source, by adding the following to your `modules_extra_content`

```
[tool.briefcase.app.my-app.linux.flatpak]
flatpak_runtime = "org.kde.Platform"
flatpak_runtime_version = "6.7"
flatpak_sdk = "org.kde.Sdk"

modules_extra_content = """
  - name: mit-krb5
    buildsystem: simple
    sources:
      - type: archive
        url: https://kerberos.org/dist/krb5/1.21/krb5-1.21.3.tar.gz
        sha256: b7a4cd5ead67fb08b980b21abd150ff7217e85ea320c9ed0c6dadd304840ad35
    build-commands:
      - cd src && autoreconf -i  # Ensure Autotools files are generated
      - cd src && ./configure --prefix=/app --disable-static --enable-shared
      - cd src && make -j$(nproc)
      - cd src && make install
"""
```
