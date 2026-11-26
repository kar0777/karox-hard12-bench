You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[FEATURE] Support MJCF slider-crank actuator transmission

## Description

`ModelBuilder.add_mjcf()` does not import actuators using `cranksite`, `slidersite`, and `cranklength`. Such actuators are omitted even though Newton already stores a two-element actuator transmission target, exposes `actuator_cranklength`, and defines `TrnType.SLIDERCRANK`.

## Expected behavior

Resolve both sites, store them in `actuator_trnid`, preserve the positive crank length and all ordinary actuator parameters, then export the actuator through MjSpec as `mjTRN_SLIDERCRANK`.

## Validation

Use a minimal slider-crank mechanism and compare the compiled transmission type, crank length, actuator length, and actuator moment against native MuJoCo at a nonzero joint pose. Missing sites and nonpositive crank lengths should produce clear errors.
