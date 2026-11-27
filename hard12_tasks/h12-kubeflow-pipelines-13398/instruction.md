You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[bug] SDK Test Failing

This SDK test is failing: https://github.com/kubeflow/pipelines/blob/master/sdk/python/kfp/cli/component_test.py#L579

```

=================================== FAILURES ===================================
_____________ Test.test_dockerfile_can_contain_custom_kfp_package ______________

self = <kfp.cli.component_test.Test testMethod=test_dockerfile_can_contain_custom_kfp_package>

    def test_dockerfile_can_contain_custom_kfp_package(self):
        component = _make_component(
            func_name='train', target_image='custom-image')
        _write_components('components.py', component)
        package_dir = os.path.dirname(os.path.dirname(self.current_dir))
    
        # suppresses large stdout from subprocess that builds kfp package
        with mock.patch.object(
                subprocess,
                'run',
                new=functools.partial(subprocess.run, capture_output=True)):
            result = self.runner.invoke(
                self.cli,
                [
                    'build',
                    str(self._working_dir), f'--kfp-package-path={package_dir}'
                ],
            )
>       self.assertEqual(result.exit_code, 0)
E       AssertionError: 1 != 0

sdk/python/kfp/cli/component_test.py:597: AssertionError
------------------------------ Captured log call -------------------------------
ERROR    root:component.py:122 Failed to find built KFP wheel under /tmp/tmpbrsaqwfx
=============================== warnings summary ===============================
```

### Steps to reproduce

- run the following command from the repo's root directory: `pytest sdk/python/kfp --ignore=sdk/python/kfp/deprecated --cov=kfp`

/area testing

