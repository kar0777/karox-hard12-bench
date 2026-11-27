You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

SQLFluff fails if directories named .sqlfluff exists

### Search before asking

- [x] I searched the [issues](https://github.com/sqlfluff/sqlfluff/issues) and found no similar issues.


### What Happened

SQLFluff changed the configuration name and the format a while ago and that default name is `.sqlfluff`.
But when putting that file into a directory called `.sqlfluff` and invoking it with the `--config` parameter results in an error:

```bash
sqlfluff lint --config .sqlfluff/.sqluff

Traceback (most recent call last):
  File "/app/.venv/bin/sqlfluff", line 8, in <module>
    sys.exit(cli())
  File "/app/.venv/lib/python3.9/site-packages/click/core.py", line 1157, in __call__
    return self.main(*args, **kwargs)
  File "/app/.venv/lib/python3.9/site-packages/click/core.py", line 1078, in main
    rv = self.invoke(ctx)
  File "/app/.venv/lib/python3.9/site-packages/click/core.py", line 1688, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
  File "/app/.venv/lib/python3.9/site-packages/click/core.py", line 1434, in invoke
    return ctx.invoke(self.callback, **ctx.params)
  File "/app/.venv/lib/python3.9/site-packages/click/core.py", line 783, in invoke
    return __callback(*args, **kwargs)
  File "/app/.venv/lib/python3.9/site-packages/sqlfluff/cli/commands.py", line 620, in lint
    config = get_config(
  File "/app/.venv/lib/python3.9/site-packages/sqlfluff/cli/commands.py", line 422, in get_config
    return FluffConfig.from_root(
  File "/app/.venv/lib/python3.9/site-packages/sqlfluff/core/config/fluffconfig.py", line 278, in from_root
    configs = load_config_up_to_path(
  File "/app/.venv/lib/python3.9/site-packages/sqlfluff/core/config/loader.py", line 316, in load_config_up_to_path
    config_stack = [load_config_at_path(str(p.resolve())) for p in config_paths]
  File "/app/.venv/lib/python3.9/site-packages/sqlfluff/core/config/loader.py", line 316, in <listcomp>
    config_stack = [load_config_at_path(str(p.resolve())) for p in config_paths]
  File "/app/.venv/lib/python3.9/site-packages/sqlfluff/core/config/loader.py", line 246, in load_config_at_path
    configs = load_config_file(p, fname, configs=configs)
  File "/app/.venv/lib/python3.9/site-packages/sqlfluff/core/config/loader.py", line 130, in load_config_file
    raw_config = load_config_file_as_dict(file_path)
  File "/app/.venv/lib/python3.9/site-packages/sqlfluff/core/config/file.py", line 103, in load_config_file_as_dict
    raw_config = _load_raw_file_as_dict(filepath)
  File "/app/.venv/lib/python3.9/site-packages/sqlfluff/core/config/file.py", line 54, in _load_raw_file_as_dict
    with open(filepath, mode="r") as file:
IsADirectoryError: [Errno 21] Is a directory: '/sql/.sqlfluff'
```

### Expected Behaviour

SQLFluff should honor the `--config .sqlfluff/.sqlfluff` before evaluating the default configuration file.

### Observed Behaviour

SQLFluff ignores the `--config .sqlfluff/.sqluff` statement and tries to check if the default configuration file exists by checking if it is a file.

### How to reproduce

This can be reproduced using:

```bash
mkdir .sqlfluff
echo '[sqlfluff]' >> .sqlfluff/.sqlfluff

docker run -it --rm -v $PWD:/sql sqlfluff/sqlfluff:3.3.0 lint --config .sqlfluff/.sqlfluff
```


### Dialect

Does not matter

### Version

```bash
$ sqlfluff --version
sqlfluff, version 3.3.0
```

### Configuration

`.sqlfluff`:

```bash
[sqlfluff]
```

### Are you willing to work on and submit a PR to address the issue?

- [ ] Yes I am willing to submit a PR!

### Code of Conduct

- [x] I agree to follow this project's [Code of Conduct](https://github.com/sqlfluff/sqlfluff/blob/main/CODE_OF_CONDUCT.md)

