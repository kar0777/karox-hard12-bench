You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[ECS] Does RunTask support capacityProviderStrategy?

Hi,

I'm trying to test a call to ecs.RunTask with a capacityProviderStrategy argument (and no launchType). The capacityProvider specified is using an autoScalingGroup. This is supposed to use autoscaling to create instances for the tasks, but I'm getting `Exception: No instances found in cluster test-cluster` when I do this. Looking at the code it seems like the runTask method doesn't use the capacityProviderStrategy argument, so I'm suspecting that this mode of operation is not supported. Is that correct? 
