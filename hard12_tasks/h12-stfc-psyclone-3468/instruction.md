You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Import scripts with the same name more than once (and sys.path growing)

While debugging some odd behaviour in one of my tests, I realised that while running tests `sys.path` keeps on growing - each time a script is executed, a path is added, but never removed (not to mention we also add empty paths ... over and over :)  ).

I am wondering if it's worth avoiding this (i.e. keeping a copy of `sys.path` before calling `load_script`, then resetting it after execution of the script).

I also looked at removing the script symbol (`del trans_func` after calling it).

None of this is expected to have a real issue for an application, since they will call PSyclone only once with one script (even Fab uses subprocesses, i.e. you always get a clean `sys.path`).

The growing `sys.path` could in theory affect parallel testing (e.g. if we have one test expecting NOT to find a script of a given name, but accidentally a previous test adds a path that has a script with that name) - which is what I though was happening in my case:

I had three tests, each providing a script with the same name but slightly different behaviour. Each individual test worked, but when I executed them all (in parallel or not), some of them would fail. Reason of course is that the first executed script imported the script, and all further imports are fulfilled from the (Python internal) cached copy - no matter if we do a `del trans_func` (which removes the symbol, but NOT the cached import), and/or clean up `sys.path`. Fix for me was easy, just use three different names.

So, summary, we have thing with testing that we have to be careful about (different tests using the same script name), but can't fix it (there seems to be no way to affect the imported cache, unless we try using `reimport`??). 

The clean up (sys.path and removing the symbol) feels nice, but doesn't do anything. TBH, it feels like we should (at least) fix sys.path ;) But that's just me being ... peculiar about this :)  I am happy if we agree to just close this issue, but equally happy to clean up sys.path (and/or the symbol, but that makes probably even less sense ;) ). I will try to add a sentence or two to the docs as part of my script args PR otherwise.
