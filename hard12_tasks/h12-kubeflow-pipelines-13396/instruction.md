You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[feature] Implement debug-pause type capabilities into SDK

### Feature Area

<!-- Uncomment the labels below which are relevant to this feature: -->
/area backend
/area sdk


### What feature would you like to see?
Argo workflows has a feature `debug-pause` that allows users to pause a workflow step for debugging purposes. This pause can occur before or after the step runs. Additionally, the after version has an option to only trigger on failure. The user can then interact with the pod with kubectl exec. Currently, KFP does not allow users to implement this feature on their components via the SDK. Adding this feature would be a powerful new tool for developers and end users as it would give additional flexibility for investigating their pipelines. We have tested adding the env vars manually into IRs and the feature does work. However, we should make this native to KFP SDK.

This proposal adds the ability to include a new function into the SDK `kfp.kubernetes.enable_debug_pause()`. This function would be applicable to tasks defined in a pipeline. The function accepts before, after, and on_error_only parameters to configure which pause mode is applied. Once applied, the function adds one of the following env vars to the task based on the user's configuration: `ARGO_DEBUG_PAUSE_BEFORE`,
 `ARGO_DEBUG_PAUSE_AFTER`, or `ARGO_DEBUG_PAUSE_ON_ERROR`. This will then be detected by Emissary and the respective behavior will be followed. Once debugging is complete, the user releases the pod by running `kubectl exec <pod> -c main -- sh -c "touch /var/run/argo/ctr/main/proceed"`.
 
 ### Alternate Design
 An alternate consideration should be made about implementing this outside of argo workflows and the native debug pause implementation. The question being, could we pause our component in a way such that we aren't restricted by the structure and format of the argo workflows architecture. One option to do this would be to implement this via a pause in the `launcher` directly that occurs once the python code is done running. This would allow us to pause within the `launcher` itself, as opposed to `emissary` which is where `debug-pause` gets checked and triggered. While there is a theoretical benefit of shelling into the environment while the `launcher` process is still alive, since both `emissary` and `launcher` run on the same container the filesystem and environment are identical either way, providing no meaningful additional debugging capability. There is added complexity of making changes to the backend as well to implement this vision.

### What is the use case or pain point?

Feature would allow developers and end users to shell into and interact with a component after it is done running. This would allow for greatly increased debugging, component understand and investigation, and accessibility for our developers and end users. 

### Is there a workaround currently?

Without this feature users cannot systematically pause their component. 

@zazulam @droctothorpe 
---

<!-- Don't delete message below to encourage users to support your feature request! -->
Love this idea? Give it a 👍. 
