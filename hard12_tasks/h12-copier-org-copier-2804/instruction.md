You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

support group file exclusion under a single condition

### Actual Situation

we have a single copier template for multiple types of deployments (thus multiple github actions pipelines), which lead us to a copier.yaml file that repeats the same condition per line on multiple lines, making it harder to update track. 


### Desired Situation

I want the copier.yaml exclude section to support group exclusions

### Proposed solution

So I'm proposing we support doing group exclusions:
```
- |
  {% if flag %}
  a.txt
  b.txt
  {% endif %}
- file-c
```
instead of

```
 - "{% if app_pipeline_disabled %}.github/workflows/deploy-type-b.yml{% endif %}"
 - "{% if app_pipeline_disabled %}.github/workflows/deploy-type-b.yml{% endif %}"
 - "{% if app_pipeline_disabled %}.github/workflows/security-check.yml{% endif %}"
....
```

