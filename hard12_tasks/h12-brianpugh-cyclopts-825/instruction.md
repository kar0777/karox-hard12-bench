You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

`test_collection_option_repeats` fails on ARM Linux

Feel free to close this, as it is probably a bug in Zsh, but I still wanted to report it

```py
________________________ test_collection_option_repeats ________________________

zsh_tester = <function zsh_tester.<locals>._make_tester at 0xfffff2fdb600>

    def test_collection_option_repeats(zsh_tester):
        """A ``list[Path]`` keyword option must accept repeated ``--file``.
    
        Without ``*`` prefix on the spec, zsh would refuse to complete a second
        ``--file`` value, breaking the natural ``--file a --file b --file c``
        usage of collection-typed parameters.
        """
        import os
        import tempfile
        from pathlib import Path as _Path
    
        app = App(name="files")
    
        @app.default
        def m(file: Annotated[list[_Path], Parameter(help="files")] = []):  # noqa: B006
            """Files."""
    
        tester = zsh_tester(app, "files")
        with tempfile.TemporaryDirectory() as td:
            (_Path(td) / "first.txt").write_text("x")
            cwd = _Path.cwd()
            try:
                os.chdir(td)
>               completions = tester.get_completions("files --file first.txt --file ")
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

/build/source/tests/completion/test_zsh.py:1187: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
/build/source/tests/completion/conftest.py:347: in get_completions
    child.expect("ZTEST> ", timeout=1.5)
/nix/store/9ccpx4wji5vh733zamz6lhxvplz05kx1-python3.13-pexpect-4.9.0/lib/python3.13/site-packages/pexpect/spawnbase.py:354: in expect
    return self.expect_list(compiled_pattern_list,
/nix/store/9ccpx4wji5vh733zamz6lhxvplz05kx1-python3.13-pexpect-4.9.0/lib/python3.13/site-packages/pexpect/spawnbase.py:383: in expect_list
    return exp.expect_loop(timeout)
           ^^^^^^^^^^^^^^^^^^^^^^^^
/nix/store/9ccpx4wji5vh733zamz6lhxvplz05kx1-python3.13-pexpect-4.9.0/lib/python3.13/site-packages/pexpect/expect.py:179: in expect_loop
    return self.eof(e)
           ^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <pexpect.expect.Expecter object at 0xfffff2f923c0>
err = EOF('End Of File (EOF). Exception style platform.')

    def eof(self, err=None):
        spawn = self.spawn
    
        spawn.before = spawn._before.getvalue()
        spawn._buffer = spawn.buffer_type()
        spawn._before = spawn.buffer_type()
        spawn.after = EOF
        index = self.searcher.eof_index
        if index >= 0:
            spawn.match = EOF
            spawn.match_index = index
            return index
        else:
            spawn.match = None
            spawn.match_index = None
            msg = str(spawn)
            msg += '\nsearcher: %s' % self.searcher
            if err is not None:
                msg = str(err) + '\n' + msg
    
            exc = EOF(msg)
            exc.__cause__ = None # in Python 3.x we can use "raise exc from None"
>           raise exc
E           pexpect.exceptions.EOF: End Of File (EOF). Exception style platform.
E           <pexpect.pty_spawn.spawn object at 0xfffff3163250>
E           command: /nix/store/8kd19j6n9qh9iq89d7d0xdvnsfjam1zw-zsh-5.9/bin/zsh
E           args: [b'/nix/store/8kd19j6n9qh9iq89d7d0xdvnsfjam1zw-zsh-5.9/bin/zsh', b'-i']
E           buffer (last 100 chars): ''
E           before (last 100 chars): '\x1b[?2004hfiles --file first.txt --file '
E           after: <class 'pexpect.exceptions.EOF'>
E           match: None
E           match_index: None
E           exitstatus: None
E           flag_eof: True
E           pid: 1249
E           child_fd: 13
E           closed: False
E           timeout: 5
E           delimiter: <class 'pexpect.exceptions.EOF'>
E           logfile: None
E           logfile_read: None
E           logfile_send: None
E           maxread: 2000
E           ignorecase: False
E           searchwindowsize: None
E           delaybeforesend: 0.05
E           delayafterclose: 0.1
E           delayafterterminate: 0.1
E           searcher: searcher_re:
E               0: re.compile('ZTEST> ')

/nix/store/9ccpx4wji5vh733zamz6lhxvplz05kx1-python3.13-pexpect-4.9.0/lib/python3.13/site-packages/pexpect/expect.py:122: EOF
--------------------------- snapshot report summary ----------------------------
24 snapshots passed.
=========================== short test summary info ============================
FAILED tests/completion/test_zsh.py::test_collection_option_repeats - pexpect.exceptions.EOF: End Of File (EOF). Exception style platform.
========== 1 failed, 2375 passed, 6 skipped, 16 deselected in 42.86s ===========
```
