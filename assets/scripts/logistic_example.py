import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import pymc3 as pm


def main():

    # format the data
    # see http://blog.yhat.com/posts/logistic-regression-python-rodeo.html
    df = pd.read_csv("../../assets/data/binary.csv")
    df.columns = ["admit", "gre", "gpa", "prestige"]
    dummy_ranks = pd.get_dummies(df['prestige'], prefix='prestige')
    cols_to_keep = ['admit', 'gre', 'gpa']
    data = df[cols_to_keep].join(dummy_ranks.ix[:, 'prestige_2':])
    data['intercept'] = 1.0

    # frequentist logistic regression
    train_cols = data.columns[1:]
    logit = sm.Logit(data['admit'], data[train_cols])
    result = logit.fit()
    print(result.summary())

    # Bayesian logistic regression #1
    with pm.Model():

        betas = pm.Normal(name="betas", sd=2.5, shape=len(train_cols), testval=0)
        mu = pm.math.matrix_dot(data[train_cols].values, betas)
        p = pm.math.sigmoid(mu)
        pm.Bernoulli(name="Y", p=p, observed=data["admit"].values)
        trace = pm.sample(11000, tune=1000, chains=2)
        print(pm.summary(trace))
        print(pm.stats.waic(trace))
        print(pm.stats.loo(trace))

    # Bayesian logistic regression #2
    with pm.Model():
        betas = pm.Normal(name="betas", sd=2.5, shape=len(train_cols), testval=0)
        mu = pm.math.matrix_dot(data[train_cols].values, betas)
        # sd = pm.HalfCauchy(name="sd", beta=2.5)
        Yhat = pm.Normal(name="Yhat", mu=mu, sd=1, shape=data["admit"].shape)
        p = pm.math.sigmoid(Yhat)
        pm.Bernoulli(name="Y", p=p, observed=data["admit"].values)
        trace = pm.sample(11000, tune=1000, chains=2)
        print(pm.summary(trace, var_names=["betas"]))
        print(pm.stats.waic(trace))
        print(pm.stats.loo(trace))


if __name__ == '__main__':

    main()
