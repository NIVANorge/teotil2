import itertools

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sn
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.preprocessing import StandardScaler


def best_subsets_ols_regression(df, resp_var, exp_vars, standardise=False):
    """Performs all possible regressions involving exp_vars and returns the one with
        the lowest AIC.

        NOTE: This approach is generally a poor choice, since repeatedly comparing
        many models leads to problems with "multiple comparisons" and essentially
        invalidates any p-values. Use with caution!

        Also note that performance will be poor with many 'exp_vars', because this
        function performs an exhaustive search of all possible combinations (rather
        than just some, as with e.g. stepwise regression).

    Args:
        df:          Dataframe
        resp_var:    Str. Response variable. Column name in 'df'
        exp_vars:    List of str. Explanatory variables. Column names in 'df'
        standardise: Bool. Whether to standardise the 'exp_vars' by subtracting the
                     mean and dividing by the standard deviation

    Returns:
        Tuple (model_result_object, scalar). A residuals plot is also shown. The
        result object is for the "best" model found; the 'scalar' is a scikit-learn
        StandardScaler() object that can be used to transform new data for use with
        the returned model.
    """
    y = df[[resp_var]]
    X = df[exp_vars]

    scaler = StandardScaler()
    if standardise:
        X = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)

    aics = {}
    for k in range(1, len(exp_vars) + 1):
        for variables in itertools.combinations(exp_vars, k):
            preds = X[list(variables)]
            preds = sm.add_constant(preds)
            res = sm.OLS(y, preds).fit()
            aics[variables] = res.aic

    # Get the combination with lowest AIC
    best_vars = list(min(aics, key=aics.get))

    # Print regression results for these vars
    preds = X[list(best_vars)]
    preds = sm.add_constant(preds)
    res = sm.OLS(y, preds).fit()
    print("Regression results for the model with the lowest AIC:\n")
    print(res.summary())

    # Plot best AIC model and residuals
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))

    axes[0].plot(df[resp_var], res.fittedvalues, "ro")
    axes[0].plot(df[resp_var], df[resp_var], "k-")
    axes[0].set_xlabel("Observed", fontsize=16)
    axes[0].set_ylabel("Modelled", fontsize=16)

    sn.histplot(res.resid, ax=axes[1], kde=True)
    axes[1].set_xlabel("Residual", fontsize=16)
    axes[1].set_ylabel("Frequency", fontsize=16)

    plt.tight_layout()

    return (res, scaler)
