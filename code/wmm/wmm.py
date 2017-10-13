import numpy as np
import pymc3 as pm
import theano.tensor as tt
import matplotlib.pyplot as plt
import util
from theano import dot
from patsy import dmatrix


def wmm_morey_cowan(data, formulae, scale=2.5):
    """Constructs a Morey--Cowan-style model for measuring working-memory
    capacity from change-detection tasks.

    Args:
        data (pd.DataFrame): Data formatted in the appropriate way.
        formulae (dict): Dictionary of formulae. A constant is used for any
            missing formulae.
        scale (float): Scale value for hyperpriors.

    Returns:
        None: Model is placed in context, ready for sampling.

    """

    # 'Pivot' long-form data. Safe to re-pivoting pivoted data.

    data = util.pivot(data, formulae)

    # Make a dict out of the formulae.

    param_names = ['kappa', 'gamma', 'zeta']
    params = {}
    dic = {p: '1' for p in param_names}
    dic.update(
        {f.split('~')[0].replace(' ', ''): f.split('~')[1] for f in formulae}
    )

    print(data)


    for p in param_names:

        # Place linear model on mu of parameter.

        dm = dmatrix(dic[p], data)
        X = np.asarray(dm)
        covs = dm.design_info.column_names
        vecbeta = []

        # Make regression coefficients.

        for cov in covs:

            # Make nicely formatted name for coefficient.

            c = ''.join(i for i in cov if i not in '"\',$')
            name = r'$\beta_{(\%s)_\mathrm{%s}}$' % (p, c)

            beta = pm.Cauchy(name=name, alpha=0, beta=scale)
            vecbeta.append(beta)

        mu = dot(X, tt.stack(*vecbeta))

        # Make delta vector of parameter.

        name = r'$\delta_{(\%s)}$' % p
        X = np.asarray(util.dmforoffsets(data))
        delta = pm.Cauchy(name=name, alpha=0, beta=scale, shape=X.shape[1])
        delta = dot(X, delta)

        # Make sigma of parameter.

        sigma = pm.HalfCauchy(name=r'$\sigma_{(\%s)}$' % p, beta=scale)

        # Make the paramater.

        params[p] = pm.Deterministic(r'$\%s$' % p, mu + delta * sigma)

    # Transform parameters into meaningful decision parameters.

    k = pm.Deterministic(
        '$k$', tt.max((params['kappa'], np.zeros(len(data))), axis=0)
    )
    g = pm.Deterministic('$g$', pm.invlogit(params['gamma']))
    z = pm.Deterministic('$z$', pm.invlogit(params['zeta']))

    # Calculate hit and false-alarm probabilities.

    q = tt.min((k / data.M.values, np.ones(len(data))), axis=0)
    f = (1 - z) * g + z * (1 - q) * g
    h = (1 - z) * g + z * q + z * (1 - q) * g

    # likelihoods

    pm.Binomial(name='$H$', p=h, n=data.D.values, observed=data.H.values)
    pm.Binomial(name='$F$', p=f, n=data.S.values, observed=data.F.values)


def main():

    with pm.Model():

        data = util.get_toy_data()
        formulae = [
            'kappa ~ 1',
            'gamma ~ 1',
            'zeta ~ 1'
        ]
        wmm_morey_cowan(data, formulae)
        # backend = pm.backends.Text('wmm')
        trace = pm.sample()
        pm.traceplot(trace)
        plt.savefig('traceplot.png')


if __name__ == '__main__':

    main()
