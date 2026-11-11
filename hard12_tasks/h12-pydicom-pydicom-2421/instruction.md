You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Add a warning when multiples of the same element are present at a given dataset level

I recently ran into an issue where a DICOM file had multiples of the same element in a sequence item. pydicom would read the file fine, but only the latter element would make it into the dataset due to using element tags as keys in the dict. It took me longer than it should've to figure out why dcmdump was showing a different sequence and check what was happening in a hex editor.

I think it'd make sense to at least warn when duplicates are found and take the first instance, rather than the last.
