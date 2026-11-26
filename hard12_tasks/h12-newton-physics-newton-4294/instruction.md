You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[BUG] Incorrect order in coupling_harvest_proxy_particle_forces()

### Bug Description

I wanted to point out some odd behavior I noticed while debugging the Newton experimental coupling framework between VBD and MPM in coupling_harvest_proxy_particle_forces(): Warp’s mesh_eval_position() uses (u, v, 1-u-v) for triangle vertices (0, 1, 2), but Newton’s harvesting kernel applies those weights to (1, 2, 0), seemingly shifting the force onto the wrong vertex. I then noticed the same ordering in fill_collider_coupling_matrices().

I’ve attached a small unit test covering the public harvesting function and a short video using Newton’s native VBD/MPM coupler. The test fails on stock Newton 1.6 with Warp 1.17, and the video compares stock behavior with the weight order corrected in both locations.

https://github.com/user-attachments/assets/bbf7283a-3e37-425f-9b47-ad2cc3ed21bb

### Reproduction Script

```python
TBD
```

### System Information

- Newton: 1.6
- Warp: 1.17
