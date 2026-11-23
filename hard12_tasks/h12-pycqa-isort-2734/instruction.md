You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Force to top should support *specific* ordering

Currently when "force to top" is being used with multiple packages, then it forces all of them to the top but unfortunately does so in an alphabetical manner.

When setting:
```toml
force_to_top = ["torch", "tensorflow"]
```

The result will be:
```py
import tensorflow
import torch
```

whereas it should be:
```py
import torch
import tensorflow
```

Currently, it seems that `isort` does not support the ability to set multiple imports at the top of a section *with a user-specified* ordering. This is prohibitive because, unfortunately, some python packages have strict order import requirements.

I hope that I'm missing something! Any idea on how to solve this with `isort` would be much appreciated!

