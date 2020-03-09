from urllib.request import urlopen
import numpy as np
import pandas as pd
import pymc3 as pm
import theano.tensor as tt
import matplotlib.pyplot as plt
from pymc3.math import dot
from itertools import product
from patsy import dmatrix


def get_rouder_data():
    """Download the data from Rouder et al.'s 2008 PNAS paper data.

    Returns:
        pd.DataFrame: Rouder et al. data.

    """
    f = "https://raw.githubusercontent.com/PerceptionCognitionLab/data0/master/wmPNAS2008/lk2clean.csv"
    data = pd.read_csv(urlopen(f), index_col=0)
    data = data[["sub", "prch", "N", "ischange", "resp", "oldcol"]]
    # data["obs"] = data["sub"]
    # data["prob_different"] = data.prch
    # data["colour"] = data.oldcol
    # data["set_size"] = data.N
    # data["different_trials"] = data.ischange
    # data["same_trials"] = 1 - data.ischange
    # data["hits"] = data.ischange * data.resp
    # data["false_alarms"] = (1 - data.ischange) * data.resp
    # data = data[
    #     [
    #         "subject",
    #         "prob_different",
    #         "colour",
    #         "set_size",
    #         "different_trials",
    #         "same_trials",
    #         "hits",
    #         "false_alarms",
    #     ]
    # ]
    print(data.columns)
    return data


#
# def compress(data, formulae):
#     """Compress the data frame so that all trials belonging to a unique
#     condition are represented by a single row in the data frame. It is safe to
#     apply this to a data frame more than once.
#
#     Args:
#         data (pd.DataFrame): Long-form data.
#         formulae (list): List of patsy-style formula.
#
#     Returns:
#         pd.DataFrame: Compressed data.
#
#     """
#     a = ["subject"]
#     b = ["set_size", "different_trials", "same_trials", "hits", "false_alarms"]
#     terms = []
#
#     for f in formulae:
#
#         for c in data.columns:
#
#             if c not in a + b and c in f and c not in terms:
#
#                 terms.append(c)
#
#     data = pd.pivot_table(data, index=a + terms + b[:1], aggfunc=np.sum)
#     data = data.drop(
#         [c for c in data.columns if c not in a + b + terms], axis=1
#     ).reset_index()
#     cartesian = product(data.columns.tolist(), data.columns.tolist())
#     ok = all((x not in y) for x, y in cartesian if x != y)
#     assert ok, "The name of an independent variable is a subset of another."
#     return data[a + list(terms) + b]
#
#
# def dm_for_lower_stochastics(data):
#     """Every subject/condition combination needs its own stochastic node.
#     Usually this would be trivial to implement, because that would be each row
#     in the data frame. Unfortunately for working-memory tasks this is not the
#     case, because subjects are presented with multiple set sizes per condition.
#     We DON'T want a stochastic node for every set size. I think that the most
#     efficient way to implement this is to create a vector of offset variables
#     and pair them to the correct rows using a new design matrix. This should
#     deal with imbalances in the data (e.g., if not every subject was tested
#     with every set size per condition).
#
#     Args:
#         data (pd.DataFrame): Compressed data.
#
#     Returns:
#         patsy.dmatrix: Design matrix.
#
#     """
#
#     not_these = ["set_size", "different_trials", "same_trials", "hits", "false_alarms"]
#     terms = [c for c in data.columns if c not in not_these]
#     formula = "0+" + ":".join("C(%s)" % t for t in terms)
#     return dmatrix(formula, data)
#
#
# def wmcap_morey_cowan(data, formulae, scale=5):
#     r"""Constructs a Bayesian hierarchical model for the estimation of working-
#     memory capacity, bias, and lapse rate using the method described by Morey
#     for Cowan-style change detection tasks. This is a "fixed-effects" version
#     of the model, which is best suited to studies with between-subjects
#     designs.
#
#     Args:
#         data (pd.DataFrame): Data.
#         formulae (list): List of patsy-style formulae; e.g.,
#             `kappa ~ C(subject)`. Accepts up to three formulae for $\kappa$,
#             $\gamma$, and/or $\zeta$. Missing formulae with default to an
#             intercept-only model.
#         scale (float): A scale parameter for all the stochastic nodes. Defaults
#             to `5`.
#
#     Returns:
#         None: All model components are placed in the context.
#
#     """
#
#     # "Compress" the data so we can create the correct amount stochastic nodes
#     # later on.
#
#     data = compress(data, formulae)
#
#     # Make a dictionary out of the formulae so they can be indexed easier.
#
#     param_names = ["kappa", "gamma", "zeta"]
#     dic = {p: "1" for p in param_names}
#     dic.update({f.split("~")[0].replace(" ", ""): f.split("~")[1] for f in formulae})
#
#     # Loop over parameters in the decision model. This is just less code than
#     # hard-coding each one.
#
#     for p in param_names:
#
#         # Construct a linear model for the predictions on the parameter.
#
#         dm = dmatrix(dic[p], data)
#         X = np.asarray(dm)
#         covs = dm.design_info.column_names
#         beta = []
#
#         # Make regression coefficients for the linear model.
#
#         for cov in covs:
#
#             # Nicely format the name of the coefficient.
#
#             c = "".join(i for i in cov if i not in "\"',$")
#             name = r"$\beta_{(\%s)_\mathrm{%s}}$" % (p, c)
#             beta.append(pm.Cauchy(name=name, alpha=0, beta=scale))
#
#         # Make the predictions of the linear model on the parameter.
#
#         mu = dot(X, tt.stack(*beta))
#
#         # Make delta vector of parameter.
#
#         name = r"$\delta_{(\%s)}$" % p
#         dm_ = dm_for_lower_stochastics(data)
#         X_ = np.asarray(dm_)
#         delta_ = pm.Normal(name=name, mu=0, sd=1.0, shape=X_.shape[1])
#         delta = dot(X_, delta_)
#
#         # Make sigma of parameter.
#
#         sigma = pm.HalfCauchy(name=r"$\sigma_{(\%s)}$" % p, beta=scale)
#
#         # Make the parameter.
#
#         dic[p] = pm.Deterministic(r"$\%s$" % p, mu + delta * sigma)
#
#     # Transform parameters into meaningful decision parameters.
#
#     zeros = np.zeros(len(data))
#     k = pm.Deterministic("$k$", tt.max((dic["kappa"], zeros), axis=0))
#     g = pm.Deterministic("$g$", pm.invlogit(dic["gamma"]))
#     z = pm.Deterministic("$z$", pm.invlogit(dic["zeta"]))
#
#     # Calculate hit and false-alarm probabilities.
#
#     q = tt.min((k / data.set_size.values, zeros + 1), axis=0)
#     f = (1 - z) * g + z * (1 - q) * g
#     h = (1 - z) * g + z * q + z * (1 - q) * g
#
#     # Construct the Likelihoods.
#
#     pm.Binomial(
#         name="$H$", p=h, n=data.different_trials.values, observed=data.hits.values
#     )
#     pm.Binomial(
#         name="$F$", p=f, n=data.same_trials.values, observed=data.false_alarms.values
#     )


def main():

    data = get_rouder_data()
    # with pm.Model():
    #
    #     data = get_rouder_data()
    #     formulae = [
    #         "kappa ~ C(subject) + C(colour, Sum) + C(prob_different, "
    #         "Treatment(0.5))",
    #         "gamma ~ C(subject) + C(prob_different, " "Treatment(0.5))",
    #         "zeta ~ C(subject)",
    #     ]
    #     wmcap_morey_cowan(data, formulae)
    #     backend = pm.backends.Text("rouder")
    #     trace = pm.sample(draws=1000, tune=2000, trace=backend)
    #     pm.traceplot(trace)
    #     plt.savefig("rouder_example/traceplot.png")


if __name__ == "__main__":

    main()
