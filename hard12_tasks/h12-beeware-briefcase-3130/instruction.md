You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Add ability to define a "default" app for a project

### What is the problem or limitation you are having?

Briefcase allows for the definition of multiple applications in a single project. When this is done, `briefcase run` requires a `-a` argument to specify which application is going to be run. 

However, in many cases, there will be a reasonable default application to run. As a convenience, it would be helpful to be able to flag an application as a default so that it will start without the need for a `-a` argument. 


### Describe the solution you'd like

An app should be able to declare:

```
[tool.briefcase]
default-app = "firstapp"
...

[tool.briefcase.app.firstapp]
...
[tool.briefcase.app.secondapp]
...
```

With this configuration, `briefcase run` will start `firstapp`. If `default-app` is undefined, the user would get the current behavior displaying a menu asking which app to run. 

If the user specifies `default-app = "foobar"` (i.e., an app name that isn't defined), an error should be raised when the configuration is parsed.

If you run `briefcase run -a` (without specifying an app ID), you should be shown the menu, even if there is a default app defined. This matches the handling of simulators and the `-d`/`--device` option on mobile platforms.

Default app handling should apply to `briefcase dev`.


### Describe alternatives you've considered

* Status quo - always require selection of the app. A mild annoyance, but not an insurmountable one.
* Make the first app in the configuration file the default app. This would work, but is an implicit behavior, and there's no reason to believe the first app is the most important one.
* Make the `default-app` option a boolean *on the app*. This removes the source of error of mistyping the app name, at the cost of a source of error where multiple apps inadvertently declare themselves as the default. For convenience, we would need to process app-level setting to a project level setting - so we might as well define it at the project level.

### Additional context

This request comes mostly because of Toga's Testbed app (and similar Toga demonstration apps) where we need to have multiple test apps to accommodate Qt and Textual variants. 

In most cases, if you want to run the Testbed, you want to run the default GUI. You run `briefcase dev`... and you get a menu asking you which app you want to run. This is a mild annoyance - the 90% case is "run the default testbed", so we should have a way to specify that preference.
