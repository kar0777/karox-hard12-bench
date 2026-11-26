You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Internal error when parsing WHERE construct with --keep-comments or --keep-directives

PSyclone reports an internal error when parsing a valid Fortran WHERE construct, but only when either the --keep-comments or --keep-directives option is enabled. The same source is processed successfully when neither option is used.

```((.psyclone_ENES-Rise) ) vka83-nxn02@rupert:~/PSycloneHorizon/other_applications$ psyclone --keep-comments nemo-5.0/MULE/BLD/ppsrc/nemo/diaptr.f90
Failed to create PSyIR from file 'nemo-5.0/MULE/BLD/ppsrc/nemo/diaptr.f90' due to:
PSyclone internal error: Failed to find opening where construct statement in: !
  WHERE (zmsk1 /= 0._wp)
  zstr(:, jn, jp_tem) = SUM(pvtr_int(:, :, jn, jp_vtr), 2) * SUM(pvtr_int(:, :, jn, jp_tem), 2) / zmsk1
  zstr(:, jn, jp_sal) = SUM(pvtr_int(:, :, jn, jp_vtr), 2) * SUM(pvtr_int(:, :, jn, jp_sal), 2) / zmsk1
ELSEWHERE
  zstr(:, jn, jp_tem) = 0._wp
  zstr(:, jn, jp_sal) = 0._wp
END WHERE. File was treated as free form.
```


