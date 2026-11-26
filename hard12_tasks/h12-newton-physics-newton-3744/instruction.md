You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[FEATURE] Support MJCF jointinparent actuator transmission

## Description

`ModelBuilder.add_mjcf()` does not recognize the common actuator target attribute `jointinparent`. The actuator is silently omitted, even though `SolverMuJoCo.TrnType.JOINT_IN_PARENT` and the final MuJoCo enum mapping already exist.

## Why this matters

For ball and free joints, `jointinparent` expresses the actuator gear in the parent frame. It is not equivalent to an ordinary `joint` transmission once the joint rotates. Dropping or downgrading it changes generalized actuator moments.

## Proposed behavior

- Resolve `jointinparent` through the same named-joint/DOF mapping as `joint`.
- Preserve `JOINT_IN_PARENT` as a distinct transmission type and direct-control actuator.
- Export it as `mjTRN_JOINTINPARENT`.
- Compare the resulting actuator moment against native MuJoCo at a rotated ball-joint pose.
