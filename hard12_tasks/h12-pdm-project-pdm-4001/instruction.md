You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

HTTP cache is wiped for every new client since hishel 2, and concurrent hash fetching silently drops files

Since the hishel 2 upgrade (#3996, in 2.29.7) the HTTP cache is deleted every time a `PDMPyPIClient` is created. Clients created at the same time race on those deletes, and on my machine that makes `pdm lock --refresh` and `pdm export -f pylock` write some packages without any files. Both exit 0.

The cleanup loop in `PDMPyPIClient.__init__`:

```python
for cache in ["http-cache.db", ".cache/hishel"]:
    cache_db = cache_dir / cache
    if not cache_db.exists():
        for f in cache_dir.iterdir():
            if not f.name.startswith(cache):
                ...  # rmtree / unlink
```

On the first pass `http-cache.db` no longer exists after a migration, so every entry not named `http-cache.db*` is removed, including the live `.cache` directory. On the second pass no file name can start with `.cache/hishel`, so everything is removed again. A second client with the same `cache_dir` starts from an empty cache:

```python
from pdm._types import RepositoryConfig
from pdm.models.session import PDMPyPIClient

src = [RepositoryConfig(config_prefix="pypi", name="mirror", url="https://example.org/simple")]
PDMPyPIClient(sources=src, cache_dir=cache)
# cache/.cache/hishel holds data here
PDMPyPIClient(sources=src, cache_dir=cache)
# cache/ is now empty
```

`fetch_hashes` builds clients in parallel, because `BaseRepository.get_hashes` opens a finder per thread, and while one thread is still opening `.cache/hishel` another one deletes it:

```
FileNotFoundError: [Errno 2] No such file or directory: '~/Library/Caches/pdm/http/.cache'
```

The error is never shown. `fetch_hashes` runs the workers with `executor.map` and never reads the results, so it is dropped and the candidate keeps an empty hash list. `pylock.py` clears the hashes before refetching, which is how packages end up with no `wheels` or `sdist`. Which packages are hit changes from run to run:

```
export 1 missing: ['mdurl', 'pygments']
export 2 missing: ['mdurl', 'packaging']
export 3 missing: ['mdurl', 'pluggy']
```

Same with the lockfile. One `pdm lock --refresh` run left `packaging`, `pluggy` and `requests` with no `files` in `pdm.lock`.

