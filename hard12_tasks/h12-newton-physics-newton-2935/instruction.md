You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[BUG] Selection API link names contains duplicated body names when articulation has close loop

### Bug Description


When same body 1 appears under multiple joints
selection api's link_name will duplicate them number of joint times, and link_names it becomes unreliable source to reference the order/indices of the links

Though interestly enough `frequency_layouts[self.root_view.model.AttributeFrequency.BODY]` will still be accurate source to get de-duplicated link names that follows right link data order.


Here is reproducing script,

```
# SPDX-FileCopyrightText: Copyright (c) 2026 The Newton Developers
# SPDX-License-Identifier: Apache-2.0

"""Reproduce duplicate leaf link names in Newton's articulation selection.

This is a minimal Newton-only reproduction of the Digit/Lab failure mode where
an articulation view resolves multiple distinct bodies to the same leaf link
name.  The real Digit asset has closed-loop / mimic structure that produces
three ``*_leg_toe_roll`` bodies per side in Newton, while Lab's contact sensor
body names are deduplicated to one per side.
"""

from __future__ import annotations

from collections import Counter

import warp as wp

import newton
from newton.selection import ArticulationView


TOE_ROLL_BODY_LABELS = [
    "World/Digit/left/main/left_leg_toe_roll",
    "World/Digit/left/loop_a/left_leg_toe_roll",
    "World/Digit/left/loop_b/left_leg_toe_roll",
    "World/Digit/right/main/right_leg_toe_roll",
    "World/Digit/right/loop_a/right_leg_toe_roll",
    "World/Digit/right/loop_b/right_leg_toe_roll",
]


def _leaf_name(label: str) -> str:
    return label.rsplit("/", 1)[-1]


def _add_digit_like_articulation() -> newton.Model:
    builder = newton.ModelBuilder()
    body_ids = []
    joint_ids = []
    inertia = wp.mat33(0.2, 0.0, 0.0, 0.0, 0.2, 0.0, 0.0, 0.0, 0.2)

    for index, label in enumerate(TOE_ROLL_BODY_LABELS):
        body_id = builder.add_link(label=label, mass=1.0, inertia=inertia)
        body_ids.append(body_id)

        if index == 0:
            joint_id = builder.add_joint_free(parent=-1, child=body_id, label="root")
        else:
            joint_id = builder.add_joint_revolute(
                parent=body_ids[index - 1],
                child=body_id,
                axis=wp.vec3(0.0, 0.0, 1.0),
                label=f"toe_roll_chain_{index}",
            )
        joint_ids.append(joint_id)

    builder.add_articulation(joint_ids, label="Digit")
    return builder.finalize()


def _body_names_from_layout(view: ArticulationView) -> list[str]:
    layout = view.frequency_layouts[view.model.AttributeFrequency.BODY]
    indices = None if layout.indices is None else layout.indices.numpy()
    slice_start = 0 if layout.slice is None else layout.slice.start

    body_names = []
    for body_id in range(view.link_count):
        local_body_id = int(indices[body_id]) if indices is not None else slice_start + body_id
        model_body_id = layout.offset + local_body_id
        body_names.append(_leaf_name(view.model.body_label[model_body_id]))
    return body_names


def _deduplicate_preserving_order(names: list[str]) -> list[str]:
    deduplicated_names = []
    seen = set()
    for name in names:
        if name not in seen:
            deduplicated_names.append(name)
            seen.add(name)
    return deduplicated_names


def main() -> None:
    model = _add_digit_like_articulation()
    view = ArticulationView(model, "Digit", include_links="*_leg_toe_roll")

    layout_body_names = _body_names_from_layout(view)
    deduplicated_sensor_like_names = _deduplicate_preserving_order(layout_body_names)

    print("Full Newton model.body_label entries selected by the view:")
    for index, label in enumerate(model.body_label):
        print(f"  {index:02d}: {label}")

    print("\nArticulationView.link_names:")
    for index, name in enumerate(view.link_names):
        print(f"  {index:02d}: {name}")

    print("\nBODY frequency-layout lookup:")
    for index, name in enumerate(layout_body_names):
        print(f"  {index:02d}: {name}")

    duplicate_counts = {name: count for name, count in Counter(layout_body_names).items() if count > 1}
    print(f"\nDuplicate leaf counts: {duplicate_counts}")

    print("\nContact-sensor-like deduplicated body names:")
    for index, name in enumerate(deduplicated_sensor_like_names):
        print(f"  {index:02d}: {name}")

    print("\nShape mismatch reproduced:")
    print(f"  articulation velocity columns: {len(layout_body_names)}")
    print(f"  contact sensor columns:        {len(deduplicated_sensor_like_names)}")
    print(
        "\nThis is the Newton-side equivalent of multiplying "
        "[num_envs, 6] articulation body velocities by [num_envs, 2] contacts."
    )


if __name__ == "__main__":
    main()
```


### Reproduction Script

```python

```

### System Information

_No response_
