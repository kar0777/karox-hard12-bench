You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

bug(packaging): [all] and doctor report an unsupported incomplete audio install as healthy

## Summary

A clean install of the local wheel with `[all]` can contain an unsupported/incomplete audio stack while `rapid-mlx doctor` reports audio as healthy.

## Environment

- Local wheel built from `main` at `93981cf4` (package version `0.11.0`)
- macOS 26.5.2, Apple M3 Ultra 256 GB
- Python 3.12

## Observed behavior

A clean `[all]` install pulled in:

```text
mlx-vlm==0.6.3
mlx-audio==0.4.6
```

`mlx-audio` arrived transitively through `mlx-vlm`. This is above Rapid-MLX's explicit `[audio]` constraint (`mlx-audio<0.4.4`) and `[all]` did not install the rest of the audio dependencies such as misaki/spaCy/phonemizer.

Despite that, `rapid-mlx doctor` reported:

```text
✓ mlx-audio (audio extras) 0.4.6
```

There is also a contract mismatch: the project metadata describes `[all]` as the union of vision/chat/embeddings, while user-facing docs describe it as “Everything above.”

## Expected behavior

- `[all]` should have one unambiguous documented meaning.
- If it claims to include audio, it should install the complete supported audio dependency set.
- `doctor` should validate the supported version range and required imports/dependencies instead of treating the presence of `mlx-audio` alone as healthy.
