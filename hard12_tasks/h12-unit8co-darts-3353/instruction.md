You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Support quantile-sorted sample averaging in NaiveEnsembleModel to prevent 1/sqrt(M) variance shrinkage on probabilistic forecasts

### Is your feature request related to a problem?

When `NaiveEnsembleModel.predict(n, num_samples > 1)` is called on $M$ probabilistic models (`predict_likelihood_parameters=False`), `NaiveEnsembleModel._target_average()` averages the unsorted Monte Carlo sample trajectories across the $M$ models:

```python
# darts/models/forecasting/naive_ensemble_model.py (lines 143-151)
for idx_target in range(n_components):
    target_values[:, idx_target] = prediction_values[
        :,
        range(
            idx_target,
            n_forecasting_models * n_components,
            n_components,
        ),
    ].mean(axis=1)
```

Because each constituent model draws `num_samples` independent random samples $Y^{(m)}_{t, c, s} \sim F^{(m)}_{t, c}$ along `axis=2`, averaging sample index $s$ across the $M$ models computes the distribution of the **sample mean of $M$ independent random variables**:

$$\bar{Y}_{t, c, s} = \frac{1}{M} \sum_{m=1}^{M} Y^{(m)}_{t, c, s}$$

whose variance shrinks by a factor of $1/M$ (and standard deviation / prediction interval width shrinks by $1/\sqrt{M}$):

$$\text{Var}(\bar{Y}) = \frac{1}{M^2} \sum_{m=1}^{M} \text{Var}(Y^{(m)})$$

#### Concrete consequences

1. **Severe under-coverage of prediction intervals**: Even if an ensemble is constructed from $M=4$ identical probabilistic models each predicting $\mathcal{N}(\mu, \sigma^2)$, `NaiveEnsembleModel.predict(n, num_samples=1000)` produces $\mathcal{N}(\mu, \sigma^2 / 4)$ — cutting the standard deviation and the `[q05, q95]` prediction interval width in **half** ($1/\sqrt{4} = 0.5$).
2. **Inconsistency between `num_samples > 1` and `predict_likelihood_parameters=True`**:
   When `predict_likelihood_parameters=True` is used on `QuantileRegression` models, `NaiveEnsembleModel._params_average()` averages the predicted quantiles directly across models ($\bar{Q}(\tau) = \frac{1}{M}\sum_{m=1}^M Q^{(m)}(\tau)$, known as **Vincentization** / quantile averaging). Under `_params_average()`, combining $M$ models with distribution $\mathcal{N}(\mu, \sigma^2)$ preserves $\mathcal{N}(\mu, \sigma^2)$ without variance shrinkage.

### Minimal reproducible example

```python
import numpy as np
from darts.datasets import AirPassengersDataset
from darts.models import LinearRegressionModel, NaiveEnsembleModel

series = AirPassengersDataset().load()
quantiles = [0.05, 0.5, 0.95]

models = [
    LinearRegressionModel(lags=12, likelihood="quantile", quantiles=quantiles, random_state=i)
    for i in range(4)
]
ens = NaiveEnsembleModel(models)
ens.fit(series)

# 1. Sampled prediction (num_samples=5000): unsorted sample averaging shrinks interval width by 1/sqrt(4) = 0.5x
pred_sampled = ens.predict(n=6, num_samples=5000)
width_sampled = (pred_sampled.quantile(0.95).values() - pred_sampled.quantile(0.05).values()).mean()

# 2. Likelihood parameter prediction: averages quantiles directly (no shrinkage)
pred_params = ens.predict(n=6, predict_likelihood_parameters=True)
width_params = (pred_params["#0_q0.95"].values() - pred_params["#0_q0.05"].values()).mean()

print(f"Sampled 90% interval width : {width_sampled:.2f}")
print(f"Quantile-averaged 90% width: {width_params:.2f}")
# Sampled 90% interval width is ~0.5x of the quantile-averaged 90% width!
```

### Describe the solution you'd like

Allow `NaiveEnsembleModel` to combine probabilistic sample predictions via **quantile averaging (sorting samples along `axis=2` before averaging across models)** or **linear opinion pool (mixture sampling)**, either via a parameter on `NaiveEnsembleModel.__init__` or by sorting samples when `num_samples > 1`:

```python
# Quantile averaging (Vincentization) in _target_average:
# Sorting along the sample axis (axis=2) aligns empirical quantiles across models
# before averaging across models (axis=1), matching _params_average() on QuantileRegression:
model_samples = prediction_values[
    :,
    range(idx_target, n_forecasting_models * n_components, n_components),
    :,
]
if prediction.n_samples > 1 and self.sort_samples:  # or reduction="quantile_average"
    model_samples = np.sort(model_samples, axis=2)
target_values[:, idx_target] = model_samples.mean(axis=1)
```

Sorting along `axis=2` before `.mean(axis=1)` is a 1-line operation, preserves marginal quantile calibration (matching `_params_average()` as `num_samples` grows), and avoids the $1/\sqrt{M}$ variance collapse when combining probabilistic models.

