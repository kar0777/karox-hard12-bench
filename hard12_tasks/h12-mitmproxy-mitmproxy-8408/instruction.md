You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Add launch_edge() to the Browser addon?

#### Problem Description

The Browser addon (mitmproxy/addons/browser.py) supports launching an
isolated, proxy-configured instance of Chrome or Firefox via
`browser.start`, but has no equivalent for Microsoft Edge. Users who
don't have Chrome or Firefox installed -- e.g. Windows users, where
Edge is always pre-installed -- currently have no working option.

#### Proposal
Add launch_edge(), following the exact same pattern as launch_chrome()
and launch_firefox(), wired into the browser.start dispatcher. I have a
working implementation with tests ready to submit if this is welcome.

#### Alternatives

#### Additional context


