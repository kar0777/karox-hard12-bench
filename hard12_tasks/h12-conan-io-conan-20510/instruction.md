You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[bug] `conan.tools.sbom` misclassifies descriptive license text containing `with` as an SPDX expression

### Describe the bug

Conan 2.34.0 treats any license text containing `AND`, `OR`, or `WITH`, in any capitalization, as an SPDX expression. This bug is found in [_is_expr](https://github.com/conan-io/conan/blob/ef323a63d3382c47e6a59c07d2d999f6a2e3af1e/conan/tools/sbom/cyclonedx.py#L205). This can classify ordinary descriptive text as an expression even when it is not valid SPDX syntax.

For example, `oda-ifc-dynamic/27.5.0` uses the license text:
> Third-party license with OpenDesignAlliance

### How to reproduce it

With Conan 2.34.0 installed, run:
```python
from types import SimpleNamespace
from conan.tools.sbom.cyclonedx import _calculate_licenses

component = SimpleNamespace(
    conanfile=SimpleNamespace(
        license="Third-party license with OpenDesignAlliance"
    )
)
print(_calculate_licenses(component))
```

Actual result
The helper classifies the text as an expression:
```json
[{"expression": "Third-party license with OpenDesignAlliance"}]
```

Expected result
Because the text is not a valid SPDX expression, represent it as a named license:
```json
[{"license": {"name": "Third-party license with OpenDesignAlliance"}}]
```

While some CycloneDX parsers may accept the invalid SPDX expression, since it passes JSON schema validation, a tool that validates SPDX expressions will still fail.
