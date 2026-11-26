You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Wrong logp in LKJ prior

As we know, LKJ prior with parameters n, p defines a distribution over p-by-p correlation matrices. When n = 1, it is uniform over all such matrices. As n goes large, the distribution becomes more concentrated around the identity matrix.

To illustrate this bug, let's restrict our attention to the case where p = 2. 
From [this paper (page 6)](http://www.sciencedirect.com/science/article/pii/S0047259X09000876), we know that Pr[R] \propto |R|^(n-1). For 2-d correlation matrices, |R| is apparently maximized at R = I, when |R| = 1. All other R has 0 < |R| < 1.

So if we increase n (> 1), \sum_{R} |R|^(n-1) decreases, and Pr[I] = (|I|^(n-1)) / (\int_{R} |R|^(n-1)) should increase.

However, 

```
>>> import pymc3 as pm
>>> f = theano.function([], pm.LKJCorr.dist(1, 2).logp(np.array([0])))
>>> f()
array(0.6931471824645996)
>>> f = theano.function([], pm.LKJCorr.dist(10, 2).logp(np.array([0])))
>>> f()
array(-0.5664327677286938)
>>> f = theano.function([], pm.LKJCorr.dist(100, 2).logp(np.array([0])))
>>> f()
array(-1.728976562499895)
```

