You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Try- except block in the gridsearch

**Is your feature request related to a current problem? Please describe.**
Yes, this is kind of a bug in the gridsearch method. There is no Try- except block in the source code which is failing to try different parameters. In particular for ARIMA model which is a wrapper of Arima model coming from statsmodels. If I pass a list of p,q,ds and P,Q,Ds as parameters, Arima model from statsmodels fail to run in every unique combination. However, many of the combinations are valid and work. Due to lack of try-except block in the gridsearch method in Darts, if a single combination fails to run whole gridsearch fails to give any output of successful combinations.   

**Describe proposed solution**
Implement Try- except block in the gridsearch and return results from the successful parameters combination. 


