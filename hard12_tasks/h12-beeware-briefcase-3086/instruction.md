You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Ability to customize MSI conclusion page

### What is the problem or limitation you are having?

As of today there is no option in Briefcase when building Windows MSI installers to customize the final page of the installer (the page shown when setup finishes). For comparison with `constructor` that builds `.exe` installers, it would be nice if I could customize:
- Custom title and body text on the final page.
- A "launch app" checkbox that runs the app when the installer closes.
- Custom checkboxes with custom behavior, e.g. a checkbox that, when checked, opens a webpage after the installer closes.

### Describe the solution you'd like

Add support for customizing the final page of the MSI installer, similar to what we already have for the EXE installer:

- A config option for custom text on the final page.
- A config option for an optional checkbox with custom text.
- A way to run an action when that checkbox is checked and the installer closes (e.g. opening a URL).

I believe WiX already supports this kind of customization natively, so this would be a matter of exposing it through Briefcase's config and template.

### Describe alternatives you've considered

None.

### Additional context

For example this is what we have today with our Miniconda .exe installer:

<img width="611" height="471" alt="Image" src="https://github.com/user-attachments/assets/0a0df32e-1249-4c41-93f1-e97d6bfbcc1b" />

And for other installers it can also launch the app if configured.
