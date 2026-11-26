You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Adding a forward folding estimator for estimating spectral profiles

The current `FluxProfileEstimator` uses backward folding to estimate the flux in different regions.
An alternative way would be to have a forward folding approach - assume a constant spatial model in the whole region, and fit the spectra model to obtain the flux in each region bin.

This has some distinct advantages, eg: allowing for the contributions of additional source models, correctly accounting for the PSF leakage, or creating a spectral index map.

A prototype implementation by @registerrier maybe found here: https://gist.github.com/registerrier/e5bc8a2939807521b1b59dff9f666b89

It can be interesting to expose this to users. We can either

1. Add a new estimator. We already have the `TSMapEstimator` and the `ExcessMapEstimator` implementing forward folding vs unfolding resp.). One issue here might be to to have the correct format for returning the results. Variations in index (or other parameters like the cutoff energy, etc) cannot be accomodated into our existing region based sky maps format. This is similar to the issue we faced for having an estimator for Time Resolved Spectroscopy.
2. Otherwise, we can simply add a notebook exposing this, like we have for the timing case.

Preferences @adonath @QRemy @bkhelifi @Astro-Kirsty ?
