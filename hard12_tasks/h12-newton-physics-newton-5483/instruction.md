You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[REQ] Replace hard-coded MuJoCo joint-type constants in the SolverMuJoCo kernels with an enum

### Description

`newton/_src/solvers/mujoco/kernels.py` compares MuJoCo joint types against integer literals with a comment naming the constant, for example `jnt_type[jnt] == 0  # mjJNT_FREE` and `jnt_type[mjc_jnt] >= 2  # mjJNT_SLIDE or mjJNT_HINGE`, and the same in `update_jnt_reference_kernel` and `update_joint_transforms_kernel`. Replace the literals with a named enum. No behavior change.

### Motivation / Use Case

Raised in review of #5312 (https://github.com/newton-physics/newton/pull/5312#discussion_r4584359624): the literals are hard to read and nothing checks them against MuJoCo's values.

### Alternatives Considered

`kernels.py` is loaded without MuJoCo installed (MJCF/USD import pulls in `SolverMuJoCo`, and `mujoco`/`mujoco-warp` are only in the `sim` extra), and `mujoco.mjtJoint` is a pybind11 enum that Warp kernels cannot parse. That leaves two options:

1. A private `IntEnum` mirror of `mjtJoint` in `newton/_src/solvers/mujoco/enums.py`, pinned against `mujoco.mjtJoint` by a test, as `TestActuatorTypes` does for the actuator-type mirrors. The name must not clash with Newton's `JointType`, which `kernels.py` already imports.
2. `mujoco_warp.JointType`, which is an `IntEnum` and works in kernels, with the affected kernels created lazily after the MuJoCo import, as `_import_contact_force_fn` does today.

