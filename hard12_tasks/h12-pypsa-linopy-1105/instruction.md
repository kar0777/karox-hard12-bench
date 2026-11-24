You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

CPLEX: Optimal solution with unscaled infeasibilities is thrown out

Hi everyone, I have an issue with CPLEX. for some problems, which Highs can solve, I get an unknown status from linopy, with the message that the problem is optimal with unscaled infeasibilities. As I understand, CPLEX introduced the solution of the scaled problem to the unscaled problem, and there were some slight infeasibilities, which usually do not mean a lot (see for examle here: http://iea-etsap.org/forum/showthread.php?tid=162)

Linopy, however, seems to not import this solution, potentially because the status is unknown and not optimal. Would it be possible to change this, so that linopy simply imports this solution, even though there might be slight infeasibilities?

Best,
Georg 
