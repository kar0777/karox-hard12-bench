You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

AttributeError: module 'docling' has no attribute '__version__'

### Bug
<!-- Describe the buggy behavior you have observed. -->
AttributeError: module 'docling' has no attribute '__version__'

### Steps to reproduce
<!-- Describe the sequence of steps for reproducing the bug. -->
1. pip install docling
2. python -c "import docling; print(docling.__version__)"
3. 
```
Traceback (most recent call last):
  File "<string>", line 1, in <module>
AttributeError: module 'docling' has no attribute '__version__'
```
4. run command `docling --version`
5. 
```
from docling.cli.main import app
ModuleNotFoundError: No module named 'docling.cli.main'

```

### Docling version
<!-- Copy the output of `docling --version`. -->
2.108, latest version

### Python version
<!-- Copy the output of `python --version`. -->
3.12.12

<!-- ⚠️ ATTENTION: When sharing screenshots, attachments, or other data make sure not to include any sensitive information. -->

