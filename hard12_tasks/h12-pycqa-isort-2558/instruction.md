You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

NOQA adds extra space characters

I was using the `multi_line_output = 7` option to prevent long imports lines from wrapping onto new lines, and I noticed that on the first run it added the NOQA comment to the end of long lines, and that was fine. However on subsequent runs it would insert an extra two spaces before the NOQA comment (unexpected and undesired):

```
-from my_package.my_module import super_long_file_name as super_long_alias  # NOQA
+from my_package.my_module import super_long_file_name as super_long_alias    # NOQA
```


I tried using the `honor_noqa = true` option to change this behavior and leave the existing NOQA comments as is. This did prevent the insertion of the extra space characters, however it also caused all the NOQA imports to be grouped together in their separate group, which is not desired.

As a workaround I ended up removing both of those settings (`multi_line_output` and `honor_noqa`), and instead I added the `line_length = 200` option as a hacky way to not wrap long lines. This worked for my needs.

But I just wanted to report the unintended behavior here to let you know.

FYI here are all the settings I ended up with:

```
[tool.isort]
force_sort_within_sections = true
single_line_exclusions = ['typing']
lexicographical = true
group_by_package = true
order_by_type = false
known_first_party = ["my_package"]
#multi_line_output = 7
#honor_noqa = true
force_single_line = true
line_length = 200
```
