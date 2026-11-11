You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Improve documentation and error handling around SSL configuration variables

### What is the problem or limitation you are having?

Originally reported by @lrandersson as #3109.

As of #3056, Briefcase uses `httpx2` to manage HTTP downloads. `httpx2` has a much stronger default certificate configuration, and Briefcase is now in a position to honor common SSL and proxy configuration environment variables.

However
1. This isn't documented, and
2. Some of the failure modes of these external configurations can be confusing. #3109 reported that if `SSL_CERT_FILE` is defined, but points at a non-existent file, a somewhat opaque `FileNotFoundError` is raised.


### Describe the solution you'd like

* Add documentation for the SSL configuration variables that Briefcase will honor. This is [the same list as httpx2](https://pydantic.dev/docs/httpx2/api/environment_variables/#ssl_cert_file). We don't need to reproduce the httpx2 docs - we only need to list that there are 6 configuration variables that can be used for HTTP configuration, and give a brief description of the purpose of each; we can defer to the httpx2 docs for full details. It would make sense to collect these variables in a subsection of the existing [environment variable docs](https://briefcase.beeware.org/en/stable/reference/environment/#environment-variables)
* If `SSL_CERT_FILE` is defined and points at a non-existent file, Briefcase should surface a more helpful error message.
* Other obvious failure modes (e.g., `HTTPS_PROXY` that doesn't exist, `SSL_CERT_DIR` that doesn't exist) should be verified, and similar error handling applied.

### Describe alternatives you've considered

No real alternative.

### Additional context

_No response_
