import numpy as np
import pymc3 as pm
import theano.tensor as tt
import matplotlib.pyplot as plt
import util
from theano import dot
from patsy import dmatrix


def make_wmm_cowan(data, formulae, scale=2.5):

    # create dict containing formulae with intercept-only added for missing

    param_names = ['kappa', 'gamma', 'zeta']
    fdic = util.formuale_list_to_dic(formulae, param_names)
    params = {}

    for p in param_names:

        # linear model

        dm = dmatrix(fdic[p], data)
        X = np.asarray(dm)
        covs = dm.design_info.column_names
        vecbetas = []

        for cov in covs:

            c = ''.join(i for i in cov if i not in '"\',$')
            beta = pm.Cauchy(
                name=r'$\beta_{(\%s)_\mathrm{%s}}$' % (p, c), alpha=0,
                beta=scale
            )
            vecbetas.append(beta)

        mu = dot(X, tt.stack(*vecbetas))

        """Offsets: we want one of these per subject and condition, but not
        necessarily per set size or per row in the data frame. I used a couple
        of little tricks to implement this efficiently and with little code,
        which unfortunately is not very readable."""

        [c for c in df.columns if c in ols.formula]
        terms = [c for c in dm.design_info.term_names if
                'subj' not in c and 'Intercept' not in c]
        f = '0+(%s):C(subj)' % '+'.join(terms)
        dm = dmatrix(f, data)
        X = np.asarray(dm)
        delta = pm.Cauchy(
            name='$\delta$', alpha=0, beta=scale, shape=(X.shape[1],)
        )
        delta_br = dot(X, tt.stack(*delta))

        # scale

        sigma = pm.HalfCauchy(name=r'$\sigma_{(\%s)}$' % p, beta=scale)

        # make the transformed decision parameter

        params[p] = pm.Deterministic(r'$\%s$' % p, mu + delta_br * sigma)

    # transform into meaningful decision params

    k = pm.Deterministic(
        '$k$', tt.max((params['kappa'], np.zeros(len(data))), axis=0)
    )
    g = pm.Deterministic('$g$', pm.invlogit(params['gamma']))
    z = pm.Deterministic('$z$', pm.invlogit(params['zeta']))

    # calculate hit and false-alarm probabilities

    q = tt.min((k / data.M.values, np.ones(len(data))), axis=0)
    f = (1 - z) * g + z * (1 - q) * g
    h = (1 - z) * g + z * q + z * (1 - q) * g

    # likelihoods

    pm.Binomial(name='$H$', p=h, n=data.S.values, observed=data.H.values)
    pm.Binomial(name='$F$', p=f, n=data.S.values, observed=data.F.values)


def main():

    with pm.Model():

        data = util.get_toy_data()
        formulae = [
            'kappa ~ C(subj) + C(clr)',
            'gamma ~ 1',
            'zeta ~ 1'
        ]
        make_wmm_cowan(data, formulae)
        backend = pm.backends.Text('wmm_cowan')
        trace = pm.sample()
        pm.traceplot(trace)
        plt.savefig('traceplot.png')


if __name__ == '__main__':

    main()
