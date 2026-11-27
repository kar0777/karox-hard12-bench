You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Add symmetric extension hierarchy for state exclusion (separable measurement bounds on antidistinguishability)

`toqito.state_opt.symmetric_extension_hierarchy` computes upper bounds on the probability of state **distinguishability** under separable measurements, using the symmetric-extension SDP technique of Navascués ([arXiv:0707.4398](https://arxiv.org/abs/0707.4398), *Pure State Estimation and the Characterization of Entanglement*, Phys. Rev. Lett. **100**, 070503, 2008) as applied to state discrimination in Cosentino's thesis (Equation 4.55 of [*Quantum State Local Distinguishability via Convex Optimization*](https://uwspace.uwaterloo.ca/handle/10012/9572), 2015; see also Cosentino's PRA paper [arXiv:1205.1031](https://arxiv.org/abs/1205.1031) for the related PPT-only SDP). No analogous hierarchy exists for state **exclusion**.

This is a significant gap: the hierarchy for distinguishability gives upper bounds on the SEP value, and at level 1 it recovers the PPT bound exactly. The exclusion analogue would provide upper bounds on how well Bob can *exclude* states using separable measurements — directly bounding what is achievable under LOCC for antidistinguishability.

## Background

For state exclusion under separable measurements, the SDP hierarchy has the same symmetric extension structure but with the objective flipped: instead of maximizing the sum over $k$ of $p_k \operatorname{Tr}(\rho_k \mu_k)$, we minimize it. The constraints on the extended variables $X_k$ (positivity, symmetric extension, PPT across all cuts) remain the same.

Concretely, the hierarchy at level $s$ for exclusion is:

> **minimize** the sum over $k$ from $1$ to $N$ of $p_k \langle \rho_k, \mu(k) \rangle$, **subject to** the same constraints as Eq. 4.55 of Cosentino's thesis.

At level 1 this gives the PPT exclusion bound. As $s \to \infty$, it converges to the true separable exclusion value.

This is directly relevant to the question: **when are quantum states antidistinguishable under LOCC/separable measurements?** For bipartite states with entanglement across Alice and Bob's labs, the global, PPT, and SEP exclusion values can all differ. Having this hierarchy in `|toqito⟩` would enable systematic numerical exploration of these gaps.

## What should be added

A function `symmetric_extension_hierarchy_exclusion` (or add an `objective` parameter to the existing function) that computes the exclusion analogue.

### Relevant code

- [`toqito/state_opt/symmetric_extension_hierarchy.py`](https://github.com/vprusso/toqito/blob/master/toqito/state_opt/symmetric_extension_hierarchy.py) — the distinguishability version to use as template
- [`toqito/state_opt/state_exclusion.py`](https://github.com/vprusso/toqito/blob/master/toqito/state_opt/state_exclusion.py) — the global exclusion SDP
- [Cosentino's thesis](https://uwspace.uwaterloo.ca/handle/10012/9572) — Chapter 4 for the hierarchy applied to discrimination, Chapter 5 for exclusion
- [arXiv:2206.08313](https://arxiv.org/abs/2206.08313) — Russo and Sikora, *A note on the inner products of pure states and their antidistinguishability* (background motivation)

### Why this is not a simple copy-paste

While the constraints are structurally the same, there are subtleties:
- The exclusion objective minimizes rather than maximizes — this affects SDP solver behavior and numerical stability
- The dual problem has a different structure (the dual of a minimization over PSD variables with symmetric extension constraints)
- The relationship between levels must be verified: level $s+1$ should give a tighter (higher) lower bound on exclusion error than level $s$
- For the distinguishability case, the hierarchy gives *upper* bounds that decrease with level. For exclusion, the hierarchy gives *lower* bounds on the error that increase with level. The monotonicity direction must be verified in tests.

### Acceptance criteria

- Function computes exclusion bounds at any level $s \geq 1$
- Level 1 output matches the PPT exclusion value (once issue #1520 is implemented, or verified independently)
- Tests include:
  - Three Bell states tensored with a resource state $|\tau_\epsilon\rangle$ (the same example used in the existing `symmetric_extension_hierarchy` docstring) — verify that the exclusion hierarchy values are consistent with the distinguishability values (exclusion value + distinguishability value relationships)
  - Monotonicity check: level 2 gives a value $\geq$ level 1 for the exclusion error
  - A case where SEP exclusion is strictly worse than global exclusion (demonstrates the hierarchy is doing something nontrivial)
- Docstring includes the SDP formulation and at least one worked example with known values

### Design options

Two reasonable approaches:
1. **New function** `symmetric_extension_hierarchy_exclusion` alongside the existing one
2. **Add a parameter** like `objective="distinguish"` / `objective="exclude"` to the existing `symmetric_extension_hierarchy`

Either is acceptable. Option 2 avoids code duplication but changes the existing API (the parameter should default to `"distinguish"` for backward compatibility).

### Out of scope

- Implementing the full Cosentino hierarchy for channels
- Proving convergence of the hierarchy (this is a known theoretical result)
- Combining with the eigenvalue criterion for circulant states

### Related issues

- #1520 — PPT state exclusion. The level-1 value of this hierarchy should match the PPT exclusion value implemented there. Implementations are independent: this issue can be done first and use a hand-coded PPT comparison, or it can wait on #1520. Either order is fine.

### Before starting

If you're picking this up, please consider commenting with a short design sketch (new function vs. `objective=` parameter, dual structure) before going deep. Not required — direct PRs welcome.

### Notation

A good PR should include a short note in the docstring or PR description explaining how the paper's / thesis's notation (e.g., $X_k$, $\mu(k)$, the symmetric projector $\Pi$) maps to the variables used in `toqito`.

