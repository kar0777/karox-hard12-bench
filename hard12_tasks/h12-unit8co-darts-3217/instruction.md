You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[BUG] TFM using optuna multiple jobs error AttributeError: _model_call

Hi

Im trying to run deep learning optimisation using optuna. It works fine if I have n_trails=1 however if I increase that number to say 2 I get a error AttributeError: _model_call. I have enough cpus.
The full error is shown below. If you want the code thats fine but will take be abit to seperate it all out so hoping for a easy fix.
> Traceback (most recent call last):
  File "/opt/conda/lib/python3.10/concurrent/futures/process.py", line 246, in _process_worker
    r = call_item.fn(*call_item.args, **call_item.kwargs)
  File "/opt/conda/lib/python3.10/concurrent/futures/process.py", line 205, in _process_chunk
    return [fn(*args) for args in chunk]
  File "/opt/conda/lib/python3.10/concurrent/futures/process.py", line 205, in <listcomp>
    return [fn(*args) for args in chunk]
  File "/opt/conda/lib/python3.10/site-packages/VeryForecast/VeryForcasting.py", line 572, in OptimiseDataframeParallel_wrapper
    best_model_df, final, df_models = self.OptimiseSeries(
  File "/opt/conda/lib/python3.10/site-packages/VeryForecast/VeryForcasting.py", line 348, in OptimiseSeries
    DeepLearningModels(
  File "/opt/conda/lib/python3.10/site-packages/VeryForecast/ForcastingModels.py", line 1468, in DeepLearningModels
    brnn_params = optimize_model(BlockRNNModelOptimise, "block_rnn", df, future_rts_df,past_rts_df,all_past_rts, forecast_horizon, backtest, stride[1], metric_list, metric, cpus,brrn_hparams)
  File "/opt/conda/lib/python3.10/site-packages/VeryForecast/ForcastingHelper.py", line 520, in optimize_model
    study.optimize(objective, n_trials=n_trials,n_jobs=2)
  File "/opt/conda/lib/python3.10/site-packages/optuna/study/study.py", line 451, in optimize
    _optimize(
  File "/opt/conda/lib/python3.10/site-packages/optuna/study/_optimize.py", line 103, in _optimize
    f.result()
  File "/opt/conda/lib/python3.10/concurrent/futures/_base.py", line 451, in result
    return self.__get_result()
  File "/opt/conda/lib/python3.10/concurrent/futures/_base.py", line 403, in __get_result
    raise self._exception
  File "/opt/conda/lib/python3.10/concurrent/futures/thread.py", line 58, in run
    result = self.fn(*self.args, **self.kwargs)
  File "/opt/conda/lib/python3.10/site-packages/optuna/study/_optimize.py", line 163, in _optimize_sequential
    frozen_trial = _run_trial(study, func, catch)
  File "/opt/conda/lib/python3.10/site-packages/optuna/study/_optimize.py", line 251, in _run_trial
    raise func_err
  File "/opt/conda/lib/python3.10/site-packages/optuna/study/_optimize.py", line 200, in _run_trial
    value_or_values = func(trial)
  File "/opt/conda/lib/python3.10/site-packages/VeryForecast/DeepLearningOptuna.py", line 276, in __call__
    model = BlockRNNModel(
  File "/opt/conda/lib/python3.10/site-packages/darts/models/forecasting/forecasting_model.py", line 107, in __call__
    return super().__call__(**all_params)
  File "/opt/conda/lib/python3.10/site-packages/darts/models/forecasting/block_rnn_model.py", line 409, in __init__
    super().__init__(**self._extract_torch_model_params(**self.model_params))
  File "/opt/conda/lib/python3.10/site-packages/darts/utils/torch.py", line 112, in decorator
    return decorated(self, *args, **kwargs)
  File "/opt/conda/lib/python3.10/site-packages/darts/models/forecasting/torch_forecasting_model.py", line 293, in __init__
    super().__init__(add_encoders=add_encoders)
  File "/opt/conda/lib/python3.10/site-packages/darts/models/forecasting/forecasting_model.py", line 2160, in __init__
    super().__init__(add_encoders=add_encoders)
  File "/opt/conda/lib/python3.10/site-packages/darts/models/forecasting/forecasting_model.py", line 135, in __init__
    self._model_params = self._extract_model_creation_params()
  File "/opt/conda/lib/python3.10/site-packages/darts/models/forecasting/forecasting_model.py", line 1873, in _extract_model_creation_params
    del self.__class__._model_call
AttributeError: _model_call
