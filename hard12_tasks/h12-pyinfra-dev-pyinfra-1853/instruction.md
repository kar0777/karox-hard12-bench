You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

`_env` in shell and script operations should accept HiddenValue

## Is your feature request related to a problem? Please describe

I am trying to pass some secret values via env variables. But it is getting rejected as the operator expects string values. I want to mask the secrets from getting printed in the logs.

```py
env = {"TOKEN": HiddenValue(os.getenv("..."))}
server.shell(
        commands=[
            "docker compose pull",
            "docker compose up",
        ],
        _chdir="/opt",
        _env=env,
    )
```

## Describe the solution you'd like

I want to be able to pass env dict with `HiddenValue` values. (related PR: https://github.com/pyinfra-dev/pyinfra/pull/1709)

