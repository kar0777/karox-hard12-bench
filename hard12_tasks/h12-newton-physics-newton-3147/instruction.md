You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[BUG] VBD Cables Kinetic Energy Injection at Small Radius

### Bug Description

Running the SolverVBD for cables at larger radius seems stable, but once the radius is small enough (e.g. 5mm for a 50cm long cable), the cable starts accumulating energy from somewhere after 4-5s. This did not happen in newton 1.2.1. See the attached simulation result, where the cable is simply dropped from an arbitrary height, and if the cable is not rotated, it stays in place (no accumulation of kinetic energy, printed in the reproduction script as output), but if the starting pose of the cable is slightly rotated in xy-plane, it will start moving due to some error accumulating.


https://github.com/user-attachments/assets/ea72cb66-fa0b-4f0c-8946-2d6a81300643

### Reproduction Script

```python
"""Minimal pure-Newton repro: two cables falling flat onto the ground.

Two straight cables (chains of capsule segments joined by cable joints, built with
``builder.add_rod``) are dropped horizontally onto a level floor, side by side:
one yawed 0 deg about world Z, one yawed 10 deg. They are offset in Y so they do
not touch.

Physical expectation: each should land and lie still, like a dropped rope. With the
rigid-contact-anchor bug, each capsule segment is an unstable contact (see
cylinder_two.py): a tiny perturbation is amplified instead of damped, so the
segments spuriously start rolling, the cable writhes/curls, and total kinetic
energy GROWS instead of decaying to rest.

Run (opens a GL window):
  PYTHONPATH=/home/mmichelis/Documents/newton-gilles \
    /home/mmichelis/Documents/IsaacLab-Origin/isaaclab.sh -p /tmp/cable_fall.py --viewer gl

Headless smoke test (prints the numbers):
  PYTHONPATH=/home/mmichelis/Documents/newton-gilles \
    /home/mmichelis/Documents/IsaacLab-Origin/isaaclab.sh -p /tmp/cable_fall.py --viewer null --num-frames 250
"""

import numpy as np
import warp as wp

import newton
import newton.examples

NUM_SEGMENTS = 20
SEGMENT_LENGTH = 0.5 / (NUM_SEGMENTS - 1)
RADIUS = 0.005
STRETCH_STIFFNESS = 1.0e6
STRETCH_DAMPING = 1.0e-4
BEND_STIFFNESS = 1.0e-4
BEND_DAMPING = 1.0e-4
DROP_GAP = 0.8
# (yaw about world Z [deg], Y-offset [m]) for each cable.
CABLES = [(0.0, -0.3), (10.0, 0.3)]


class Example:
    def __init__(self, viewer, args=None):
        self.viewer = viewer
        self.args = args

        self.fps = 100
        self.frame_dt = 1.0 / self.fps
        self.sim_time = 0.0
        self.sim_substeps = 8
        self.sim_dt = self.frame_dt / self.sim_substeps
        self.frame = 0

        builder = newton.ModelBuilder(gravity=-9.81, up_axis=newton.Axis.Z)

        cfg = newton.ModelBuilder.ShapeConfig()
        cfg.density = 100.0
        cfg.mu = 1.0
        cfg.ke = 1.0e3
        cfg.kd = 1.0e0
        cfg.kf = 0.0

        builder.add_shape_plane(body=-1, cfg=cfg)

        # Two horizontal cables, each yawed about world Z and offset in Y, dropped from DROP_GAP.
        length = NUM_SEGMENTS * SEGMENT_LENGTH
        start_z = RADIUS + DROP_GAP
        self.cables = []  # list of (label, body indices)
        for yaw_deg, y_off in CABLES:
            yaw = np.radians(yaw_deg)
            direction = wp.vec3(float(np.cos(yaw)), float(np.sin(yaw)), 0.0)
            center = wp.vec3(0.0, float(y_off), start_z)
            start0 = center - 0.5 * length * direction
            pts = newton.utils.create_straight_cable_points(
                start=start0, direction=direction, length=length, num_segments=NUM_SEGMENTS
            )
            edge_q = newton.utils.create_parallel_transport_cable_quaternions(pts, twist_total=0.0)
            bodies, _ = builder.add_rod(
                positions=pts,
                quaternions=edge_q,
                radius=RADIUS,
                cfg=cfg,
                stretch_stiffness=STRETCH_STIFFNESS,
                stretch_damping=STRETCH_DAMPING,
                bend_stiffness=BEND_STIFFNESS,
                bend_damping=BEND_DAMPING,
                label=f"cable_{yaw_deg:g}deg",
            )
            self.cables.append((f"{yaw_deg:g}deg", bodies))

        builder.color()
        self.model = builder.finalize()

        self.solver = newton.solvers.SolverVBD(
            self.model,
            iterations=20,
            rigid_contact_k_start=1.0e1,
            rigid_avbd_beta=1.0e2,
        )

        self.state_0 = self.model.state()
        self.state_1 = self.model.state()
        self.control = self.model.control()
        self.contacts = self.model.contacts()

        self.viewer.set_model(self.model)
        self.graph = None
        self.masses = self.model.body_mass.numpy()
        self.inertias = self.model.body_inertia.numpy()
        names = ", ".join(n for n, _ in self.cables)
        print(f"two cables ({names}); {NUM_SEGMENTS} segments each, length {length:.2f} m, radius {RADIUS} m")

    def _stats(self, q, qd, bodies):
        idx = np.array(bodies)
        mean_h = float(np.mean(q[idx, 2]))
        max_v = float(np.max(np.linalg.norm(qd[idx, 3:6], axis=1)))
        ke = 0.0
        for b in bodies:
            w, v = qd[b, 0:3], qd[b, 3:6]
            ke += 0.5 * float(self.masses[b]) * float(v @ v) + 0.5 * float(w @ (self.inertias[b] @ w))
        return mean_h, max_v, ke

    def simulate(self):
        for _ in range(self.sim_substeps):
            self.state_0.clear_forces()
            self.viewer.apply_forces(self.state_0)
            self.model.collide(self.state_0, self.contacts)
            self.solver.step(self.state_0, self.state_1, self.control, self.contacts, self.sim_dt)
            self.state_0, self.state_1 = self.state_1, self.state_0

    def step(self):
        self.simulate()
        self.sim_time += self.frame_dt
        if self.frame % 10 == 0:
            q = self.state_0.body_q.numpy()
            qd = self.state_0.body_qd.numpy()
            parts = []
            for name, bodies in self.cables:
                h, mv, ke = self._stats(q, qd, bodies)
                parts.append(f"{name}: h={h:.4f} |v|={mv:7.3f} KE={ke:.3e}")
            print(f"{self.frame:5d} | " + "  |  ".join(parts))
        self.frame += 1

    def render(self):
        self.viewer.begin_frame(self.sim_time)
        self.viewer.log_state(self.state_0)
        self.viewer.log_contacts(self.contacts, self.state_0)
        self.viewer.end_frame()


if __name__ == "__main__":
    viewer, args = newton.examples.init()
    newton.examples.run(Example(viewer, args), args)
```

### System Information

- newton: 1.3.0rc2
- warp: 1.14.0 (CUDA Toolkit 12.9)
- Python: 3.12.13
- OS: Linux 6.17.0-22 (x86_64, glibc 2.39)
- GPU: NVIDIA RTX A6000, driver 590.48.01
