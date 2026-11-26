You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Questions that are hidden by default

### Actual Situation

Our org has one big template that is used by multiple projects. Often we want to include options/features in the template that most users wouldn't/shouldn't care about and just leave as default. Cases for this include:
* Features that are still not ready for general usage, and are still under development/debugging.
* Features that you'd want to leave the default 90% of the time (for e.g. the python version to compile the docs with, in almost all cases, it's the same as the project's version, but some projects need this to be different)

Currently, standard users have to consider these questions when copying/updating into a project, leaving them frustrated since they need to fill out a lot of redundant paperwork, but still stay vigilant since they don't know which questions are important or not ahead of time.

### Desired Situation

Ideally, users would like to automatically skip these "advanced" questions, leaving them at their default value until they explicitly need to use them.

### Proposed solution

I propose adding a new key to question in `copier.yml`: `ask`. `ask` acts the same as the existing `when` key, with the exception that questions marked as `ask: false` will still be prompted if the user's `copy` or `update` command has the `--ask` flag targeting the question. Specifically:

* If a question's `when` evaluates to `false`, the question will not be asked, regardless of the command's `--ask` filters, same as current behavior.
* Otherwise, If a question matches the command's `--ask` filters, it will prompt the user to answer, same as any other question.
* Otherwise, if a question's `ask` evaluates to `false`, it will be automatically skipped, and its default/previous value, if any, will be used to render the template (same as when its `when` key evaluates to `false`)

Example:
```yaml
# copier.yml
main_branch: 'main'
docs:
  type: bool
docs_branch:
  when: "{{ docs }}"  # question is only relevant if docs are enabled
  ask: false          # but most users still don't wanna fiddle with this
                      # even if docs are enabled
  default: "{{ main_branch }}"
release_branch:
  ask: "{{ main_branch != 'main' }}  # users only want to fiddle with
                                     # this if they're not using a standard
                                     # main branch. In this usage, "ask"
                                     # is like an opt-in "when"
```

```bash
>>> copier copy gh:my_template .
# will prompt main_branch, docs, and release_branch if main_branch != main
>>> copier copy gh:my_template . --ask release_branch
# will prompt main_branch, docs, and release_branch
>>> copier copy gh:my_template . --ask docs_branch
# will prompt main_branch, docs, and release_branch if main_branch != main,
#  if `docs` is true, will also prompt docs-branch
>>> copier copy gh:my_template . --ask '*_branch'
# will prompt main_branch, docs, and release_branch,
#  if `docs` is true, will also prompt docs-branch
```
