You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Jinja error without clear filename

### Describe the problem

I run copier and get a stacktrace without filename. That super hard to debug. 


### Template

just an empty dir (you can add files, but this is minimal): 


```
mkdir -p 'my-template/some-{{{{ jinja_error }}}}'

```

### To Reproduce

```
mkdir -p 'my-template/some-{{{{ jinja_error }}}}'

# note we have no copier file, so by default it assumes "{{" escape pattern

copier copy my-template .
```

### Logs

```console
copier copy template generated --trust

Copying from template version None
Traceback (most recent call last):
  File "/opt/homebrew/bin/copier", line 8, in <module>
    sys.exit(CopierApp.run())
             ^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/plumbum/cli/application.py", line 640, in run
    inst, retcode = subapp.run(argv, exit=False)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/plumbum/cli/application.py", line 635, in run
    retcode = inst.main(*tailargs)
              ^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/copier/_cli.py", line 284, in main
    return _handle_exceptions(inner)
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/copier/_cli.py", line 71, in _handle_exceptions
    method()
  File "/opt/homebrew/lib/python3.11/site-packages/copier/_cli.py", line 275, in inner
    with self._worker(
  File "/opt/homebrew/lib/python3.11/site-packages/copier/_main.py", line 271, in __exit__
    raise value
  File "/opt/homebrew/lib/python3.11/site-packages/copier/_cli.py", line 282, in inner
    worker.run_copy()
  File "/opt/homebrew/lib/python3.11/site-packages/copier/_main.py", line 95, in _wrapper
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/copier/_main.py", line 1039, in run_copy
    self._render_template()
  File "/opt/homebrew/lib/python3.11/site-packages/copier/_main.py", line 717, in _render_template
    for dst_relpath, ctx in dst_relpaths_ctxs:
  File "/opt/homebrew/lib/python3.11/site-packages/copier/_main.py", line 931, in _render_path
    yield from self._render_parts(relpath.parts, is_template=is_template)
  File "/opt/homebrew/lib/python3.11/site-packages/copier/_main.py", line 885, in _render_parts
    rendered_part = self._render_string(part, extra_context=extra_context)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/copier/_main.py", line 945, in _render_string
    tpl = self.jinja_env.from_string(string)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/jinja2/environment.py", line 1111, in from_string
    return cls.from_code(self, self.compile(source), gs, None)
                               ^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/lib/python3.11/site-packages/jinja2/environment.py", line 771, in compile
    self.handle_exception(source=source_hint)
  File "/opt/homebrew/lib/python3.11/site-packages/jinja2/environment.py", line 942, in handle_exception
    raise rewrite_traceback_stack(source=source)
  File "<unknown>", line 1, in template
jinja2.exceptions.TemplateSyntaxError: expected token ':', got '}'
```

### Expected behavior

I would get a clear filename/directory name that cannot be templated. The stack trace is ugly already, but `File "<unknown>", line 1, in template` is hard. 

### Screenshots/screencasts/logs

_No response_

### Operating system

macOS

### Operating system distribution and version

MacOS

### Copier version

copier 9.9.0

### Python version

python3.13

### Installation method

uvx+pypi

### Additional context

_No response_
