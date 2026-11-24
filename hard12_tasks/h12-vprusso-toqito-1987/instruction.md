You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

is_quantum_channel returns False for channels whose input and output dimensions differ

## Before reporting this bug:
- [x] Verify there is not an existing issue for it already
- [x] You are using the latest version of `toqito` with a Python version `>=3.12`

## Describe the bug
`is_quantum_channel` returns `False` for valid channels whenever the input and output dimensions differ. This happens even when the channel is given as Kraus operators, where the dimensions are unambiguous.

When `phi` is a list, `is_quantum_channel` first converts it with `kraus_to_choi` and then calls `is_trace_preserving` on the Choi matrix without `dim`. `is_trace_preserving` then has to assume two equal subsystems, which raises a `ValueError` for e.g. a 6x6 Choi matrix (qubit to qutrit), and that error is caught and returned as `False`. Calling `is_completely_positive` and `is_trace_preserving` directly on the same Kraus operators gives `True` for both.

For a Choi matrix there is currently no way to pass the dimensions, since `is_quantum_channel` doesn't take a `dim` argument.

This also affects `channel_relative_entropy` and `channel_measured_relative_entropy`. Both take `in_dim` and compute `out_dim = n // in_dim`, but they validate `channel_1` with `is_quantum_channel(channel_1)`, so any channel with `in_dim != out_dim` is rejected.

## To Reproduce
```python
import numpy as np
from toqito.channel_ops import kraus_to_choi
from toqito.channel_props import is_completely_positive, is_quantum_channel, is_trace_preserving

# Embedding a qubit into a qutrit: V^* V = I_2, so rho -> V rho V^* is a valid channel.
V = np.array([[1, 0], [0, 1], [0, 0]])
print(is_completely_positive([V]))  # True
print(is_trace_preserving([V]))     # True
print(is_quantum_channel([V]))      # False (expected True)

# Partial trace over the first qubit of a two-qubit system, Kraus operators <i| (x) I_2.
K = [np.kron(np.eye(2)[[i]], np.eye(2)) for i in range(2)]
print(is_quantum_channel(K))        # False (expected True)
```

And for the relative entropy:

```python
from toqito.channel_metrics import channel_relative_entropy

J1 = kraus_to_choi([V])
J2 = (J1 + np.kron(np.eye(2), np.eye(3) / 3)) / 2
channel_relative_entropy(J1, J2, in_dim=2)
# ValueError: Channel relative entropy is only defined if channel_1 is a quantum channel.
```

## Expected behavior
Both channels above should be reported as quantum channels. A possible fix:

- pass Kraus operators straight to `is_completely_positive` and `is_trace_preserving` (both already handle them) instead of converting to a Choi matrix first,
- add an optional `dim` argument to `is_quantum_channel` that is forwarded to `is_trace_preserving` for Choi matrices, and
- have the two relative entropy functions pass `dim=[in_dim, n // in_dim]`.

With that change, `channel_measured_relative_entropy` on the example above gives 0.538997, which matches -ln(7/12). (For a maximally entangled input, the output of the first channel is pure and is an eigenvector of the second channel's output with eigenvalue 1/2 + 1/12.)

I have a fix with tests ready and will open a PR.

