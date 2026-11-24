You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Formatting problems in an  `else` conditional import

Given the following code in a `.pyi` file

```python
import sys
import weakref
from typing import Any, ClassVar, overload, type_check_only

if sys.version_info >= (3, 11):
    from typing import LiteralString, Never
else:
    from typing_extensions import LiteralString
    from typing_extensions import Never
```

`isort` automatically formats it to 

```python
import sys
import weakref
from typing import Any, ClassVar, overload, type_check_only


if sys.version_info >= (3, 11):
    from typing import LiteralString, Never
else:
    from typing_extensions import LiteralString, Never  # <<< `isort`ed line
```

which is expected.

---

However, if you add additional imports below the conditional in the first example,

```python
import sys
import weakref
from typing import Any, ClassVar, overload, type_check_only

if sys.version_info >= (3, 11):
    from typing import LiteralString, Never
else:
    from typing_extensions import LiteralString
    from typing_extensions import Never

import third_party_library  # <<< Additional import
```

`isort` no longer formats the `else` conditional imports:

```python
import sys
import weakref
from typing import Any, ClassVar, overload, type_check_only


if sys.version_info >= (3, 11):
    from typing import LiteralString, Never
else:
    from typing_extensions import LiteralString  # <<< Not formatted
    from typing_extensions import Never          # <<< Not formatted

import third_party_library  # <<< Additional import
```

---

**isort version: 5.10.1**

**isort configuration**:

> [settings]
lines_before_imports=1
lines_after_imports=2
extra_standard_library=typing_extensions
profile=black
multi_line_output=3
combine_as_imports=True

