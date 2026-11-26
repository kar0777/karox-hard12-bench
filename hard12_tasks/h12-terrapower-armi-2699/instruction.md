You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Warning or error should be raised if ARMI can't find specified ISOTXS file

https://github.com/terrapower/armi/blob/f1c01a6f2155afa10e96a5f49c2ab9b91db65b71/armi/physics/neutronics/latticePhysics/latticePhysicsInterface.py#L170-L172

If you ask ARMI to copy a set of cross section files from a specific cycle and node, and ARMI can't find that file, the code does not even warn the user. It just happily continues with some other cross section file. This has the potential to introduce significant bugs that are difficult to see. At least this runLog statement should be elevated to warning. I personally think it should probably raise an error
