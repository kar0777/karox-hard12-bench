You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

ui.sub_pages with root_path claims paths outside its root (e.g. /) because the prefix is stripped without checking

### First Check

- [x] I added a very descriptive title here.
- [x] This is not a security issue (those should be reported via the [security advisory](https://github.com/zauberzeug/nicegui/security/advisories/new) instead).
- [x] This is not a Q&A. I am sure something is wrong with NiceGUI or its documentation.
- [x] I used the GitHub search to find a similar [issue](https://github.com/zauberzeug/nicegui/issues) and came up empty.

### Example Code

```python
from nicegui import APIRouter, app, ui


@ui.page('/')
def index():
    ui.label('Index page')


@ui.page('/other')
def other():
    ui.label('Other page')


router = APIRouter(prefix='/admin')


@router.page('/')
@router.page('/{path:path}')
def admin():
    ui.button('navigate.to("/")', on_click=lambda: ui.navigate.to('/'))
    ui.button('navigate.to("/other")', on_click=lambda: ui.navigate.to('/other'))
    ui.link('link to "/"', '/')
    ui.sub_pages({
        '/': lambda: ui.label('Admin overview'),
        '/users': lambda: ui.label('Admin users'),
    }, root_path='/admin')


app.include_router(router)

ui.run()
```

### Description

On a page with `ui.sub_pages(root_path='/admin')`, navigating to a path outside `/admin` does not leave the page if the rest of the path, after cutting off `len(root_path)` characters, matches one of the sub page routes. The URL changes, but the sub page content stays. This happens with `ui.navigate.to()` and with clicking a link.

Open `/admin/` and:

- click `navigate.to("/")`: the URL becomes `/`, the page still shows "Admin overview" (expected: "Index page")
- click `navigate.to("/other")`: the URL becomes `/other`, the page still shows "Admin overview" (expected: "Other page")
- click the link to `/`: same as the first case

Reloading the browser then shows the correct page.

The cause is in `SubPages._find_matching_path()` (`nicegui/elements/sub_pages.py`, line 147 in 3.18.0). It strips the root path by its length without checking that the current path starts with it:

```python
relative_path = self._router.current_path[len(self._root_path or ''):]
```

`'/'[6:]` and `'/other'[6:]` both give `''`. That is normalized to `'/'` and matches the sub page `'/'`. So `has_any_unresolved_path()` returns `False`, and `SubPagesRouter._handle_navigate()` (`sub_pages_router.py`, line 82) never calls `_other_page_builder_matches_path()`. It only pushes the new URL into the history.

Related but different: #5777 (fixed in #5886) and #6281 (fixed in #6374) both fixed the fallback in `_other_page_builder_matches_path()`, i.e. finding the other page once `ui.sub_pages` has given up on a path. Here `ui.sub_pages` never gives up, because the path outside its `root_path` is wrongly matched by its own routes.

This is independent of #6281 / #6374. The other page would be found by `_other_page_builder_matches_path()`, but that method is never reached. The behavior is the same with NiceGUI 3.17.0 and 3.18.0, and with FastAPI 0.140.6 and 0.142.4. For a target whose remainder does not match a sub page, for example `/other/page`, 3.18.0 correctly leaves the SPA.

A possible fix is to treat a path outside `root_path` as not matched:

```python
def _find_matching_path(self) -> RouteMatch | None:
    root_path = (self._root_path or '').rstrip('/')
    path = urlparse(self._router.current_path).path
    if root_path and path != root_path and not path.startswith(root_path + '/'):
        return None
    ...  # unchanged
```

Then `_handle_navigate()` falls through to `_other_page_builder_matches_path()` and opens the other page. With `show_404=True`, `_set_match(None)` would briefly render the 404 label before the browser leaves. It may be nicer not to re-render at all for a path outside the root.

As a workaround we call `context.client.open(path)` instead of `ui.navigate.to(path)`. That does not help for links, for example in Markdown content.

### NiceGUI Version

3.18.0 (also 3.17.0)

### Python Version

3.10.11

### Browser

Edge

### Operating System

Windows

### Additional Context

_No response_
