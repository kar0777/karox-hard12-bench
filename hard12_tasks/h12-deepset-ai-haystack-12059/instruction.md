You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

FileSystemToolResultStore.read() allows reading files outside the configured store root

**Describe the bug**
FileSystemToolResultStore.write() correctly restricts writes to the configured root directory, but read() accepts any filesystem path it is given. This means a caller can pass a path that was never returned by write() and still read that file if it is accessible.

**Error message**
None. No error is raised; read() returns the file contents.

**Expected behavior**
read() should only accept references that belong to the configured store root, and reject anything outside it, just like write() already does.

**Additional context**
This makes write() and read() inconsistent. It is especially relevant for tool-result offloading, where the returned value is supposed to act like a store-scoped reference, not an arbitrary filesystem path. The same issue also applies to symlinks inside the store root that point outside it.

**To Reproduce**
1. Create a `FileSystemToolResultStore` with a root directory.
2. Create a readable file outside that root.
3. Call `store.read()` with the outside file path.
4. Observe that the file content is returned.

```python
from pathlib import Path
from haystack.hooks.tool_result_offloading import FileSystemToolResultStore

root = Path("tool_results")
root.mkdir(exist_ok=True)

outside = Path("outside.txt")
outside.write_text("secret", encoding="utf-8")

store = FileSystemToolResultStore(root=root)
print(store.read(str(outside)))  # returns "secret"
```

**FAQ Check**
- [x] Have you had a look at [our new FAQ page](https://docs.haystack.deepset.ai/docs/faq)?

**System:**
- OS: macOS
- Haystack version: 3.0.0-rc0

