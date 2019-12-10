import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import pymc3 as pm
import theano.tensor as tt


def main():

    # format the data
    # see http://blog.yhat.com/posts/logistic-regression-python-rodeo.html
    df = pd.read_csv("../../assets/data/binary.csv")
    df.columns = ["admit", "gre", "gpa", "prestige"]
    dummy_ranks = pd.get_dummies(df["prestige"], prefix="prestige")
    cols_to_keep = ["admit", "gre", "gpa"]
    data = df[cols_to_keep].join(dummy_ranks.loc[:, "prestige_2":])
    data["intercept"] = 1.0

    # frequentist logistic regression
    train_cols = data.columns[1:]
    logit = sm.Logit(data["admit"], data[train_cols])
    result = logit.fit()
    print(result.summary())

    # # Bayesian logistic regression
    # with pm.Model():
    #
    #     betas = pm.Normal(name="betas", sd=2.5, shape=len(train_cols), testval=0)
    #     pi = pm.math.sigmoid(pm.math.matrix_dot(data[train_cols].values, betas))
    #     pm.Bernoulli(name="Y", p=pi, observed=data["admit"].values)
    #     trace = pm.sample(tune=2000)
    #     print(pm.summary(trace))
    #     pm.traceplot(trace, compact=True)
    #     plt.savefig("tmp1.png")

    # Bayesian liability treshold model
    with pm.Model():
        betas = pm.Normal(name="betas", sd=2.5, shape=len(train_cols), testval=0)
        psi = pm.math.matrix_dot(data[train_cols].values, betas)
        from sys import float_info
        eps = float_info.epsilon
        pi = tt.switch(psi <= 0, eps, 1.-eps)
        pm.Bernoulli(name="Y", p=pi, observed=data["admit"].values)
        trace = pm.sample(tune=2000)
        print(pm.summary(trace))
        pm.traceplot(trace, compact=True)
        plt.savefig("tmp1.png")


if __name__ == "__main__":
    main()
