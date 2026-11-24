You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

skip_gitignore=true will break ignoring directories defined in skip during filesystem traversal

### Description
When starting isort with `--skip_gitignore`, directories that should not be traversed because they are configured in `skip` will be traversed.

From what I've seen, this is purely a performance problem, so all files that should be skipped will be filtered out at some later point.

### Instructions to reproduce
Minimal setup (note: "node_modules" is in the default skip values.)
```bash
# assuming isort 5.10.1 is installed (`pip3 install isort`)
mkdir test && cd test
git init
mkdir -p node_modules/this_should_not_be_accessed
touch test.py
strace isort . 2>&1 | grep this_should_not  # as expected, not queried
strace isort --skip-gitignore . 2>&1 | grep this_should_not  # suddenly, stat and open syscalls appear
```

On a side note: Add more files, and the node_modules folder will be queried more often:

```bash
touch test2.py
strace isort --skip-gitignore . 2>&1 | grep this_should_not  # 2 stat and 2 open calls
touch test3.py
strace isort --skip-gitignore . 2>&1 | grep this_should_not  # 3 stat and 3 open calls
```

adding `node_modules` to a `.gitignore` doesn't help, even though the directory should then be double-ignored by isort (this is #1895).
```bash
echo "node_modules" >> .gitignore
strace isort --skip-gitignore . 2>&1 | grep this_should_not  # 3 stat and 3 open calls
```

### Environment & Versions
Run on ubuntu21.10 with python3.9.7. Actual syscalls probably depend on the python interpreter, if you can't reproduce, I'll probably be able to figure out what python code causes the access.


### Related Issues
Closely related to #1895, but if I undestand that issue correctly, it does not talk about `skip` at all, but just files from .gitignore. ~It seems to me that the current PR for #1895, #1900, would fix this.~
Possibly related #1762 and #1777, both read as if they were fixed.

### Background
Yesterday, I realized that `isort` takes >90 seconds to run on one project where it processes 107 files with approximately 10k lines of code. Turns out, it doesn't need 90 seconds to process, but rather 89s to traverse what feels like the entire file system, only to then do its actual work in ~1s:
```bash
time isort --show-files . > isort_output.txt
real  1m35.831s

time cat isort_files.txt | xargs isort
real 0m0.896s
```
which is absurd, considering that `black` also finds the code files and finishes in 3 seconds. I wasn't able to get `isort` to skip reading directories it really doesn't need to access (venv, node_modules, web server static files, ...)
