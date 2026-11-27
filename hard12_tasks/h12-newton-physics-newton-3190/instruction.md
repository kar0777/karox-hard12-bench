You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[BUG] ViewerFile.is_running() returns True after viewer.close() -- because it's not implemented

### Bug Description

When using `Newton.Viewer.ViewerGL`, calling `viewer.close()` changes some internal flag such that `viewer.is_running()` returns False afterwards, as would be suggested by the function names. However, this is not the case with `ViewerFile`: even after `viewer.close()` is called, `viewer.is_running()` continues to return True.

Looking at the code, this is because`ViewerFile` does not implement `is_running()`, and in `ViewerBase` the default behavior is to return True. Thus, it seems like an easy fix could be to just add a flag to `ViewerFile` to track whether `ViewerFile.close()` has been called.

This inconsistency/bug causes an issue when a main simulation loop is implemented as:
```
while viewer.is_running(): 
    ...
```
This while loop can be terminated by `viewer.close()` when `viewer` is an instance of `ViewerGL`, but this termination no longer works if `viewer` is an instance of `ViewerFile`. Being able to easily swap between viewer types while using this pattern seems like something that is worth supporting...?

I have attached a reproduction script for reproducing this issue. It is a modified version of `example_recording.py`. If you set `HEADLESS` on line 129 to True, then Newton will run with `ViewerFile`, and you will see that although the log file is saved when the max frame count is reached and thus `viewer.close()`is called, the simulation loop will continue, and frames will continue to be saved. If you set `HEADLESS` to False, then Newton will correctly terminate after the maximum frame count has been exceeded.

I can submit a PR for this soon, if this is a problem deemed worth fixing and a contribution is welcome. Just let me know!

### Reproduction Script
This is a modified version of `example_recording.py` made to show how the current lack of a `viewer.is_running()` implementation for `ViewerFile` prevents workflows that have easy switching between a GUI render mode and a headless log-file mode.

Changes were only made near the end of the file. There is a comment indicating where changes were made.

```python
# SPDX-FileCopyrightText: Copyright (c) 2025 The Newton Developers
# SPDX-License-Identifier: Apache-2.0

###########################################################################
# Example Recording
#
# Shows how to record a simulation using ViewerFile for automatic recording
# of model structure and state data during simulation.
#
# Recording happens automatically - ViewerFile captures all logged states
# and saves them when the viewer is closed.
#
# Command: python -m newton.examples recording
#
###########################################################################

import numpy as np
import warp as wp

import newton
import newton.examples


class Example:
    def __init__(self, viewer, _args):
        # Setup simulation parameters
        self.fps = 60
        self.frame_dt = 1.0 / self.fps
        self.sim_time = 0.0
        self.sim_substeps = 10
        self.sim_dt = self.frame_dt / self.sim_substeps

        self.viewer = viewer
        self.world_count = 100

        # Set numpy random seed for reproducibility
        self.seed = 123
        self.rng = np.random.default_rng(self.seed)

        start_rot = wp.quat_from_axis_angle(wp.normalize(wp.vec3(*self.rng.uniform(-1.0, 1.0, size=3))), -wp.pi * 0.5)

        mjcf_filename = newton.examples.get_asset("nv_humanoid.xml")

        articulation_builder = newton.ModelBuilder()
        articulation_builder.add_mjcf(
            mjcf_filename,
            ignore_names=["floor", "ground"],
            up_axis="Z",
        )

        # Joint initial positions
        articulation_builder.joint_q[:7] = [0.0, 0.0, 1.5, *start_rot]

        builder = newton.ModelBuilder()
        for _i in range(self.world_count):
            articulation_builder.joint_q[7:] = self.rng.uniform(
                -1.0, 1.0, size=(len(articulation_builder.joint_q) - 7,)
            ).tolist()
            builder.add_world(articulation_builder)
        builder.add_ground_plane()

        # Finalize model
        self.model = builder.finalize()
        self.control = self.model.control()

        self.solver = newton.solvers.SolverMuJoCo(
            self.model,
            use_mujoco_cpu=False,
            solver="newton",
            integrator="euler",
            iterations=10,
            ls_iterations=5,
            njmax=100,
        )

        self.state_0, self.state_1 = self.model.state(), self.model.state()

        self.use_cuda_graph = wp.get_device().is_cuda

        if self.use_cuda_graph:
            with wp.ScopedCapture() as capture:
                self.simulate()
            self.graph = capture.graph

        # Set model in viewer (ViewerFile will automatically record it)
        self.viewer.set_model(self.model)

    def simulate(self):
        for _ in range(self.sim_substeps):
            self.state_0.clear_forces()
            self.solver.step(self.state_0, self.state_1, self.control, None, self.sim_dt)
            self.state_0, self.state_1 = self.state_1, self.state_0

    def step(self):
        with wp.ScopedTimer("step", active=False):
            if self.use_cuda_graph:
                wp.capture_launch(self.graph)
            else:
                self.simulate()
        self.sim_time += self.frame_dt

    def render(self):
        self.viewer.begin_frame(self.sim_time)
        self.viewer.log_state(self.state_0)  # ViewerFile automatically records this
        self.viewer.end_frame()

    def test_final(self):
        pass


if __name__ == "__main__":
    # Create ViewerFile for automatic recording
    import sys

    recording_file = "humanoid_recording.bin"

    # Check if user wants a different filename from command line
    if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
        recording_file = sys.argv[1]

    print(f"Recording simulation to: {recording_file}")
    print("ViewerFile will automatically save when the simulation ends.")

    parser = newton.examples.create_parser()
    args = parser.parse_args()

    # -------------------------- BELOW IS THE CHANGED SECTION TO SHOW BUG --------------------------
    HEADLESS = True #CHANGE THIS TO TOGGLE BEHAVIOR
    if HEADLESS:
        viewer = newton.viewer.ViewerFile(recording_file, auto_save=False)
    else:
        viewer = newton.viewer.ViewerGL(headless=False)

    # Create example
    example = Example(viewer, args)

    # Run for a reasonable number of frames
    max_frames = 1000
    frame_count = 0

    # while frame_count < max_frames:
    while viewer.is_running():
        example.step()
        example.render()
        frame_count += 1

        if frame_count % 100 == 0:
            print(f"Frame {frame_count}/{max_frames}")
        
        if frame_count >= max_frames:
            viewer.close()


    # Close viewer (automatically saves recording)
    # viewer.close()
    print(f"Recording completed: {recording_file}")
```

### System Information

- Newton version: commit a046d613
- Python version: 3.11.14
- OS: Ubuntu 24.04.3
- Kernel: 6.17.0-29 generic
- GPU: RTX4070 mobile
- Nvidia driver: 580.159.03
- CUDA version: 13.0

