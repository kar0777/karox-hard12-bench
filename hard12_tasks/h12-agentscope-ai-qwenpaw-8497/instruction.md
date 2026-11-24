You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[Bug]: Plugin hot-install aborts when importlib.invalidate_caches() raises on distro-patched Python 3.11（我的插件被这个卡了））

## QwenPaw Version

2.2.2

## Description

The plugin loader calls `importlib.invalidate_caches()` unconditionally at three
sites (`loader.py:201`, `loader.py:465`, `loader.py:1094`). On Python builds where
this stdlib function itself raises (a real-world distro backport bug, see
Additional Notes), the exception propagates and aborts the entire plugin
install / hot-update.

Cache invalidation is best-effort by design — a failure here should not be fatal.

**Related PR(s):** N/A
**Security considerations:** None

## Component(s) Affected

- [x] Core / Backend (app, agents, config, providers, utils, local_models)
- [ ] Console (frontend web UI)
- [ ] Channels (DingTalk, Feishu, QQ, Discord, iMessage, etc.)
- [ ] Skills
- [ ] CLI
- [ ] Documentation (website)
- [ ] Tests
- [ ] CI/CD
- [ ] Scripts / Deploy

## Environment

- **QwenPaw version:** 2.2.2
- **OS:** Linux x86_64 (Lifsea 8 container, kernel 5.10.134-18.0.12.lifsea8)
- **Install method:** pip (venv)
- **Python version (if applicable):** 3.11.15 (`libpython3.11-minimal 3.11.2-6+deb12u9`)

## Steps to Reproduce

1. On an affected Python build, verify the environment bug directly:

   ```bash
   python3 -c "import importlib; importlib.invalidate_caches()"
   ```

   → `TypeError: MetadataPathFinder.invalidate_caches() missing 1 required positional argument: 'cls'`

2. With QwenPaw running, install any plugin whose `requirements.txt` contains a
   not-yet-satisfied dependency (Console upload or `qwenpaw plugin install`).
3. The install aborts with the TypeError above; the plugin directory is copied
   into `plugins/` but the plugin never loads.

## Actual vs Expected

- **Actual:** The entire plugin install fails with `TypeError: MetadataPathFinder.invalidate_caches() missing 1 required positional argument: 'cls'`.
- **Expected:** A cache-invalidation failure degrades to a warning and the install proceeds.

## Logs / Screenshots

```
File ".../qwenpaw/app/routers/plugins.py", line 847, in upload_plugin
  record = await _load_plugin_with_optional_force_reinstall(...)
File ".../qwenpaw/plugins/loader.py", line 1179, in load_plugin_from_path
  record = await self._load_plugin_from_path_unlocked(...)
File ".../qwenpaw/plugins/loader.py", line 1316, in _load_plugin_from_path_unlocked
  await asyncio.to_thread(...)
File ".../qwenpaw/plugins/loader.py", line 465, in _install_requirements_locked
  importlib.invalidate_caches()
File "/usr/lib/python3.11/importlib/__init__.py", line 70, in invalidate_caches
  finder.invalidate_caches()
File "<frozen importlib._bootstrap_external>", line 1409, in invalidate_caches
TypeError: MetadataPathFinder.invalidate_caches() missing 1 required positional argument: 'cls'
```

## Additional Notes

Root cause has two layers:

1. **Environment (not QwenPaw's fault):** this distro build backported the
   CPython 3.12 change "PathFinder.invalidate_caches also clears
   importlib.metadata caches" into 3.11's frozen bootstrap, but the backported
   `/usr/lib/python3.11/importlib/metadata/__init__.py` (line 918) lost its
   `@classmethod` decorator:

   ```python
   def invalidate_caches(cls):      # ← @classmethod missing in backport
       FastPath.__new__.cache_clear()
   ```

   So **every** `importlib.invalidate_caches()` call raises. Reproduced with a
   bare interpreter, including under `python3 -S`. The same environment bug
   also breaks `pip`, `pytest`, etc., so QwenPaw cannot rely on the
   environment being fixed — it should tolerate the failure.

2. **QwenPaw side:** `loader.py:201` / `:465` / `:1094` call it unguarded.

**Suggested fix** — wrap all three sites:

```python
try:
    importlib.invalidate_caches()
except Exception:
    logger.warning("importlib.invalidate_caches() failed; continuing", exc_info=True)
```

**Workaround for plugin authors:** ship the plugin without `requirements.txt`
when all deps are already QwenPaw host dependencies — `loader.py:392` returns
early when the file is absent, bypassing the failing path entirely. (Verified:
`pyyaml>=6.0` is already a direct `Requires-Dist` of the `qwenpaw` package.)

