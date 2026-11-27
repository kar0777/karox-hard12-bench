You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[BUG] Performance issues when using parametrization on a larger report repository

### Library Version

1.1.0

### Python Version

3.11

### Operating System

Linux

### Authentication Method

Azure CLI (az login)

### What is the problem?

Deployments get a lot more slow when having a large respositories, with a bunch of files. In my case I had 58 semantic models and reports, where the reports were using the enhanced metadata format. That means that for a single report we could have over 400 json files.  

Functionally the output stayed correct, but runtime was inflated by redundant local scanning work. This made deploy cycles noticeably heavier in medium-to-large Fabric workspaces and created a scalability bottleneck in day-to-day development and CI.

When deploying the example of 58 objects, It was taking more then 2 hours and wasn't even finished.

### Steps to reproduce

Add objects to your workspace repository with a large number of files. The deployment is almost exponentially growing with each report you add.

### Expected behavior

Deployment performance should scale more predictably with actual work performed. Parameter filters should be evaluated with file-local context where possible, and repository refresh should avoid rediscovering the same filesystem structure repeatedly. The deployment lead time should be almost linear with the number of objects you are deploying.

### Actual behavior

The implementation effectively re-walked significant parts of the repository in paths that run frequently, leading to redundant I/O and path computation. Functional output remained correct, but execution time was inflated due to avoidable repeated traversal.

### Is there an ideal solution?

_No response_

### Additional context, screenshots, logs, error output, etc

_No response_
