import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pymc3 as pm
import theano.tensor as tt

from urllib.request import urlopen

from patsy import dmatrix


def main():
    """Download the Rouder et al. (2008) data set, organize it, fit the model, and
    plot the traces.

    """
    # load the data
    a = "https://raw.githubusercontent.com/PerceptionCognitionLab/"
    b = "data0/master/wmPNAS2008/lk2clean.csv"
    df = pd.read_csv(urlopen(a + b), index_col=0)

    # compress into "binomial" format
    data = []
    for (subj, N), _df in df.groupby(["sub", "N"]):

        data.append(
            {
                "subj": subj,
                "M": N,
                "H": _df[_df.ischange.astype(bool)].resp.sum(),
                "D": _df.ischange.sum(),
                "F": _df[(1 - _df.ischange).astype(bool)].resp.sum(),
                "S": (1 - _df.ischange).sum(),
            }
        )
    data = pd.DataFrame(data)
    subjects = data.subj.unique()

    # create a design matrix to map subjects to rows in data
    X = np.asarray(dmatrix("0 + C(subj)", data))

    # create model

    with pm.Model():

        # capacity
        mu = pm.Cauchy(name=r"$\mu_{(\kappa)}$", alpha=0, beta=5)
        de = pm.Normal(name=r"$\delta_{\kappa)}$", mu=0, sigma=1, shape=len(subjects))
        si = pm.HalfCauchy(name=r"$\sigma_{(\kappa)}$", beta=5)
        x = pm.Deterministic(r"$\kappa$", mu + de * si)
        x = pm.Deterministic(r"$k$", tt.largest(x, tt.zeros(len(subjects))))
        k = pm.math.dot(X, x)

        # guesses "same"
        mu = pm.Cauchy(name=r"$\mu_{(\gamma)}$", alpha=0, beta=5)
        de = pm.Normal(name=r"$\delta_{\gamma)}$", mu=0, sigma=1, shape=len(subjects))
        si = pm.HalfCauchy(name=r"$\sigma_{(\gamma)}$", beta=5)
        x = pm.Deterministic(r"$\gamma$", mu + de * si)
        x = pm.Deterministic(r"$g$", pm.math.sigmoid(x))
        g = pm.math.dot(X, x)

        # does not lapse
        mu = pm.Cauchy(name=r"$\mu_{(\zeta)}$", alpha=0, beta=5)
        de = pm.Normal(name=r"$\delta_{\zeta)}$", mu=0, sigma=1, shape=len(subjects))
        si = pm.HalfCauchy(name=r"$\sigma_{(\zeta)}$", beta=5)
        x = pm.Deterministic(r"$\zeta$", mu + de * si)
        x = pm.Deterministic(r"$z$", pm.math.sigmoid(x))
        z = pm.math.dot(X, x)

        # probabilities
        q = tt.smallest(k / data.M, tt.ones(len(data)))
        h = (1 - z) * g + z * q + z * (1 - q) * g
        f = (1 - z) * g + z * (1 - q) * g

        # responses
        pm.Binomial(name="$H$", p=h, n=data.D, observed=data.H)
        pm.Binomial(name="$F$", p=f, n=data.S, observed=data.F)

        # sample and plot
        trace = pm.sample(draws=5000, tune=2000, chains=2)
        pm.traceplot(trace, compact=True)
        plt.savefig("../../assets/images/wm-cap.png", bbox_inches=0, transparent=True)


if __name__ == "__main__":

    main()
