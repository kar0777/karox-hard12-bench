You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Sub-page parameters typed with `| None` reject values 3.18.0 accepted

### First Check

- [x] I added a very descriptive title here.
- [x] This is not a security issue (those should be reported via the [security advisory](https://github.com/zauberzeug/nicegui/security/advisories/new) instead).
- [x] This is not a Q&A. I am sure something is wrong with NiceGUI or its documentation.
- [x] I used the GitHub search to find a similar [issue](https://github.com/zauberzeug/nicegui/issues) and came up empty.

### Example Code

```python
from nicegui import ui

def a(n: int | float | None = None):
    ui.label(repr(n))

def b(n: int | str | None = None):
    ui.label(repr(n))

def c(n: int | None = None):
    ui.label(repr(n))

@ui.page('/')
@ui.page('/{_:path}')
def index():
    ui.sub_pages({'/a': a, '/b': b, '/c': c})

ui.run()
```

### Description

#6452 made `X | None` annotations convert like `Optional[X]` already did. That conversion uses only the first non-`None` member, so values 3.18.0 passed through as strings now fail:

| URL | 3.18.0 | 3.19.0 |
|---|---|---|
| `/a?n=1.5` | `'1.5'` | error |
| `/a?n=1e3` | `'1e3'` | error |
| `/b?n=abc` | `'abc'` | error |
| `/c?n=` | `''` | error |
| `/a?n=2`, `/b?n=7` | `'2'`, `'7'` | `2`, `7` |

"error" means the sub-page shows `500: sub page /a?n=1.5 produced an error` and the log has `ValueError: invalid literal for int() with base 10` from `PageArguments._convert_parameter`. `Optional[int | float]` behaved like this before 3.19 too; #6452 extended it to the `|` spelling.

Plain `@ui.page` parameters with the same annotations go through FastAPI and give `1.5`, `1000.0`, `'abc'` and `'7'`, and a 422 for `?n=` on `int | None`. Should sub-pages convert the same way? Then the first three rows would work again, `/b?n=7` would give `'7'` as on plain pages, and `?n=` on `int | None` would stay an error. Or should an empty value become `None` there?

I have a patch for either direction and can open a PR if that's welcome.

### NiceGUI Version

3.19.0

### Python Version

3.12.11

### Browser

Other

### Operating System

macOS

### Additional Context

Found by comparing v3.18.0 and v3.19.0 with the `User` fixture, so no browser is involved.

