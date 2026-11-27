You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Add option to modify specific answer when `update`ing

### Actual Situation

One of our template questions is a listing of all the internal dependencies of a project (they are excluded from min-age verifications and the like)

```yml
internal_dependencies:
  help: "Dependencies local to the org included in the project"
  default: []
```

when adding/removing an internal dependency to a project, a user has two options:
* Either they call `copier update`, and press `enter` a dozen times to update this one answer inline (the prompt is already filled in, so adding new entries to the list is easy).
* Or they call `copier update -A --data internal_dependencies=[...]` where `...` is the shorthand yaml syntax for the list (not as it appears in `.copier-answers.yml`), with the user's modification

Both are rather unwieldy

### Desired Situation

It would be easiest for to be able to skip all questions when `update`ing except for the few that the user knows ahead of time that they know they want to change.

### Proposed solution

introduce a new switch to `copier copy` named `--answer`, that the user may use to specify which questions they want to answer. acceptable values:
* `--answer=foo` answer only the question named `foo`
* `--answer=foo-*` answer only questions starting with `foo-*` (this is useful if the user wants to modify only some sub-section of the template)
* `--answer=a,b`, filters can be combined with a comma, in this case, only the questions `a` and `b` will b answered

In addition, `--answer` can include categories starting with a dollar sign, for example
* `--answer=$SHOWN` answer all non-hidden questions in the template (this can be considered the default value)
* `--answer=$UNANSWERED` answer only questions that haven't been previously answered (`-A` can be an alias for this)
* `--answer=` answer no questions (`--defaults` can be an alias for this)

When this argument is supplied to `copier copy`, it skips all questions that don't match any of the filters provided. Users can then call `copier update --answer=internal_dependencies` and they will only be prompted with the filled-in current value of `internal_dependencies`
