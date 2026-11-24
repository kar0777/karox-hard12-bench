You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Minos confidence fit not reporting failure in FluxPoint upper-limit

As discussed in the dev call/gammapyv2 paper call of Sept 25th, there are some strange behaviour of the reported upper limit computed when using `FluxPointEstimator`.

The devil is in the details and here is what we understood so far.

So when simulating a SpectrumDatasetONOFF with no source signal (pure bkg), we compute UL via the `FluxPointEstimator` and compare it to what you get with the `stat_scan`.
In theory the 95% UL is when the LL increases by 3.84 (1 dof) and the LL profile UL should match the blue curve and the horizontal dotted line in the plot below.

While this is true in most cases, it happens that the LL profile UL is not at all at that intersection even when the LL profile looks "normal".


<img width="2344" height="1748" alt="Image" src="https://github.com/user-attachments/assets/f96c6759-742c-4a6d-a33f-66bd51264543" />

This is due to the fact that internally, we rely on the Confidence function from Minos which uses brentq and does not rely on the computed `stat_scan`. 

A possible explanation is that Minos confidence failed and did not report it as the `success` attribute is `True` in this case but this related to the Fit results and not the Minos Confidence success. 
So we need to investigate if Minos Confidence failed here and find a way to report it.

The other issue is that via the Confidence Minos function, it ignores the min,max values set on the parameter (the reported UL can be negative when min was set to zero). It also ignores (wihtout telling you) the attribute `estimator.norm.scan_min` which is confusing for the user.

So we probably to understand this better, at the minimum any failure should be propagated back to the high level object to filter unsuccessful events.

