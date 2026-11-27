You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Allow opt-out of waiting for macOS notarisation

### What is the problem or limitation you are having?

macOS notarization is a process that can take between minutes and hours. When notarization runs in CI, it ties up a runner until the task times out. It would be preferable to be able to opt-out of the waiting behavior so that CI resources (especially limited macOS runners) can be conserved, rather than be spent idling waiting for a notarization response from Apple.

### Describe the solution you'd like

Add a `--no-wait` option to the macOS `package` command, disabled by default (i.e., "wait=True" is the default value.)

When `--no-wait` is specified:
1. An initial notarization request will *submit* the notarization, and write the notarization request marker file, but will *not* attempt to finalise the notarization. The user should be shown an "info" level message that is very similar to the current warning, but indicates the next step is to re-run `briefcase package` to finalise.
2. A resumed notarization request will perform exactly *one* attempt to retrieve the notarization status. If the notarization attempt does not return a canonical response (either success or failure), the command should raise an error with a "Apple has not completed notarising the app; try again later" message, rather than sleeping and trying again. The wait bar "waiting for notarization acceptance..." message should also be updated to "Checking notarization status... " in the `--no-wait` case, to reflect the "one-shot" nature of the attempt.

### Describe alternatives you've considered

* Status quo - let notarization soak up CI resources
* Raise an *error* on the initial notarization attempt. That would allow/require notarization to be a "re-run the same task until it succeeds" operation. Raising a success message means the *finalization* portion can be the only part that is re-run.

### Additional context

The argument and any related variables should be expressed as `wait`, `wait_for_finalization` etc, rather than the double-negative of `no_wait=True`

The `--no-wait` option should also be documented in the macOS guide as an option on the `package` command.
