import numpy as np
import pymc3 as pm
import theano.tensor as tt
import matplotlib.pyplot as plt
import util
from theano import dot
from patsy import dmatrix


def wmcap_morey_cowan(data, formulae, scale=5):
    r"""Constructs a Bayesian hierarchical model for the estimation of working-
    memory capacity, bias, and lapse rate using the method described by Morey
    for Cowan-style change detection tasks. This is a "fixed-effects" version
    of the model, which is best suited to studies with between-subjects
    designs.

    Args:
        data (pd.DataFrame): Data.
        formulae (list): List of patsy-style formulae; e.g.,
            `kappa ~ C(subject)`. Accepts up to three formulae for $\kappa$,
            $\gamma$, and/or $\zeta$. Missing formulae with default to an
            intercept-only model.
        scale (float): A scale parameter for all the stochastic nodes. Defaults
            to `5`.

    Returns:
        None: All model components are placed in the context.

    """

    # "Compress" the data so we can create the correct amount stochastic nodes
    # later on.

    data = util.compress(data, formulae)

    # Make a dictionary out of the formulae so they can be indexed easier.

    param_names = ['kappa', 'gamma', 'zeta']
    dic = {p: '1' for p in param_names}
    dic.update(
        {f.split('~')[0].replace(' ', ''): f.split('~')[1] for f in formulae}
    )

    # Loop over parameters in the decision model. This is just more elegant
    # than hard coding each one.

    for p in param_names:

        # Construct a linear model for the predictions on the parameter.

        dm = dmatrix(dic[p], data)
        X = np.asarray(dm)
        covs = dm.design_info.column_names
        beta = []

        # Make regression coefficients for the linear model.

        for cov in covs:

            # Nicely format the name of the coefficient.

            c = ''.join(i for i in cov if i not in '"\',$')
            name = r'$\beta_{(\%s)_\mathrm{%s}}$' % (p, c)
            beta.append(pm.Cauchy(name=name, alpha=0, beta=scale))

        # Make the predictions of the linear model on the parameter.

        mu = dot(X, tt.stack(*beta))

        # Make delta vector of parameter.

        name = r'$\delta_{(\%s)}$' % p
        dm_ = util.dm_for_lower_stochastics(data)
        X_ = np.asarray(dm_)
        delta_ = pm.Cauchy(name=name, alpha=0, beta=scale, shape=X_.shape[1])
        delta = dot(X_, delta_)

        # Make sigma of parameter.

        sigma = pm.HalfCauchy(name=r'$\sigma_{(\%s)}$' % p, beta=scale)

        # Make the parameter.

        dic[p] = pm.Deterministic(r'$\%s$' % p, mu + delta * sigma)

    # Transform parameters into meaningful decision parameters.

    zeros = np.zeros(len(data))
    k = pm.Deterministic('$k$', tt.max((dic['kappa'], zeros), axis=0))
    g = pm.Deterministic('$g$', pm.invlogit(dic['gamma']))
    z = pm.Deterministic('$z$', pm.invlogit(dic['zeta']))

    # Calculate hit and false-alarm probabilities.

    q = tt.min((k / data.set_size.values, zeros + 1), axis=0)
    f = (1 - z) * g + z * (1 - q) * g
    h = (1 - z) * g + z * q + z * (1 - q) * g

    # Construct the Likelihoods.

    pm.Binomial(name='$H$', p=h, n=data.different_trials.values,
                observed=data.hits.values)
    pm.Binomial(name='$F$', p=f, n=data.same_trials.values,
                observed=data.false_alarms.values)