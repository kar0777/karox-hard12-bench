You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

raise CloseSpider("Error Message") is not saving error message

When I run the code `raise CloseSpider("Error Message")` in the Spider **parse** function, the reason gets saved in the **finish_reason** stats string.

When it is run in the **start_requests** function, the spider properly closes but the **finish_reason** does not have the message it in.  The finish_reason value is "finished" instead of "Error Message" as set in the CloseSpider exception.

Is this intentional or a bug?  thanks!
