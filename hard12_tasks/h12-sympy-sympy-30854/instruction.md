You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

simplify regression in newer versions

```
S,K,T,t,r,sigma=symbols('S K T t r sigma')
simplify(-sqrt(2)*K*exp(-r*(T - t))*exp(-(sigma*sqrt(T - t)/2 - log(S*exp(r*(T - t))/K)/(sigma*sqrt(T - t)))**2/2)/(2*sqrt(pi)*S*sigma*sqrt(T - t)) + sqrt(2)*exp(-(sigma*sqrt(T - t)/2 + log(S*exp(r*(T - t))/K)/(sigma*sqrt(T - t)))**2/2)/(2*sqrt(pi)*sigma*sqrt(T - t)))
```

The above expression (Black–Scholes option-pricing formula) is 0. I've just started using sympy and this was one of the first examples I tried. On my older Ubuntu 12.04 with sympy 0.7.1.rc1 this correctly simplifies to zero. On newer sympy versions (0.7.4, 0.7.5) it does not simplify to zero.

