You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

git_hook(lazy=True) not checking unstaged changes

Passing `lazy=True` to `git_hook` causes isort to [_discover_ unstaged files](https://github.com/PyCQA/isort/blob/ab9cd3601d92d59416a57f457dcabb27ff622dd3/isort/hooks.py#L63-L64), but then AFAICS it still only [checks the staged file content](https://github.com/PyCQA/isort/blob/ab9cd3601d92d59416a57f457dcabb27ff622dd3/isort/hooks.py#L84-L86).

This fits with my observed behaviour that running the following in my `pre-commit` hook:
```
python -c "import sys; from isort.hooks import git_hook; sys.exit(git_hook(strict=True, modify=True, lazy=True))"
```
does not flag (or fix) isort errors in files that are modified but not staged.

AFAICS this has been broken since it was [added](https://github.com/PyCQA/isort/pull/1345) but perhaps I've missed something?
