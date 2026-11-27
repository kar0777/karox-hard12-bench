You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Pro-rata charged project should charge up to one month before end of project

This is to ensure that no charges are ever made after the end of the project, often aligning with the end of the funding. So if a project starts at some point in April and ends at some point in October, equal charges should be made from April to September (6 charges). At the moment, charges are made from April to October (7 charges), meaning that the last one is actually processed in November (on the 10th).

Probably the solution is:
- Modify [this property](https://github.com/ImperialCollegeLondon/proCAT/blob/2d8c8bedcc1aaed3a19f911685a14b34130fa70e/main/models.py#L610) to make it a function that takes the data to be processed, returning `None` if not in the right month
- Update [this function](https://github.com/ImperialCollegeLondon/proCAT/blob/2d8c8bedcc1aaed3a19f911685a14b34130fa70e/main/report.py#L65) to pass the date to the above function.
- Within the same function, make sure that the monthly charge uses the right number of months - as simple as [removing this +1](https://github.com/ImperialCollegeLondon/proCAT/blob/2d8c8bedcc1aaed3a19f911685a14b34130fa70e/main/models.py#L625).

And, obviously, fix the tests as needed.

