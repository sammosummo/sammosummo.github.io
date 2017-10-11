import numpy as np
import pymc3 as pm
import theano.tensor as tt
from util import fcn

def make_wmm_cowan(data, formulae, scale=2.5):

    formulae_dic = [f.split('~')]
    dm['z'].design_info.column_names
    sigma_kappa = pm.HalfCauchy(name='$\sigma_{(\kappa)}$', beta=scale)
    sigma_gamma = pm.HalfCauchy(name='$\sigma_{(\gamma)}$', beta=scale)
    sigma_zeta = pm.HalfCauchy(name='$\sigma_{(\zeta)}$', beta=scale)
    kappa = pm.Deterministic('$\kappa$', mu_kappa + delta_kappa * sigma_kappa)
    gamma = pm.Deterministic('$\gamma$', mu_gamma + delta_gamma * sigma_gamma)
    zeta = pm.Deterministic('$\zeta$', mu_zeta + delta_zeta * sigma_zeta)
    k = pm.Deterministic('$k$', tt.max((kappa, np.zeros(len(data))), axis=0))
    g = pm.Deterministic('$g$', pm.invlogit(gamma))
    z = pm.Deterministic('$z$', pm.invlogit(zeta))
    q = tt.min((k / data.M.values, np.ones(len(data))), axis=0)
    f = (1 - z) * g + z * (1 - q) * g
    h = (1 - z) * g + z * q + z * (1 - q) * g
    pm.Binomial(name='$H$', p=h, n=data.S.values, observed=data.H.values)
    pm.Binomial(name='$H$', p=f, n=data.S.values, observed=data.F.values)

