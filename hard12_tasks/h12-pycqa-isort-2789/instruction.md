You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

section headers and footers do not abide by comment_prefix setting

Section headers and footers do not currently abide by the comment_prefix setting, and as such, can break region folding if used for the section headers/footers as seen below.

example config:
```
comment_prefix = ""
import_heading_stdlib = "#region Standard Library"
import_footer_stdlib = "#endregion Standard Library"
```

expected output:
```
#region Standard Library

import sys

#endregion Standard Library
```

actual output:
```
# #region Standard Library

import sys

# #endregion Standard Library
```
