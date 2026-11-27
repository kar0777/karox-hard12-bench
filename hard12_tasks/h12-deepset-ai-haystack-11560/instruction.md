You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

feat: Add support to pass in a `Secret` for  `azure_endpoint` and `api_version` in `AzureOpenAIChatGenerator`

**Is your feature request related to a problem? Please describe.**

@ju-gu has a client who wants to easily switch between different `azure_endpoint` and `api_version` when going from testing in a dev environment and then deploying to prod. They are using yaml files to deploy their pipelines so it would be easiest for them if these two variable supported resolution via our `Secret` param since they would like to swap these values via environment variables.

So the point would be to keep the current string support but in addition add support for `Secret` on these two variables. 

**Additional context**
This impacts a current client of ours. Reach out to @ju-gu for more details. 

