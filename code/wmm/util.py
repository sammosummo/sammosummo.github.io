import urllib.request
import numpy as np
import pandas as pd
from patsy import dmatrix


def get_toy_data():
    """Download the Rouder et al. data. Requires internet access.

    Returns:
        pd.DataFrame: Rouder et al. data.

    """

    data = pd.read_csv(urllib.request.urlopen(
        'https://raw.githubusercontent.com/PerceptionCognitionLab/data0/' +
        'master/wmPNAS2008/lk2clean.csv'
    ))
    data = data[['sub', 'prch', 'N', 'ischange', 'resp', 'oldcol']]
    data['subj'] = data['sub']
    data['prob_D'] = data.prch
    data['colour'] = data.oldcol
    data['M'] = data.N
    data['D'] = data.ischange
    data['H'] = data.ischange * data.resp
    data['S'] = (1 - data.ischange)
    data['F'] = (1 - data.ischange) * data.resp
    data = data[['subj', 'M', 'D', 'S', 'H', 'F', 'prob_D', 'colour']]

    return data


def pivot(data, formulae):
    """Convert data from long-form to pivoted format.

    Args:
        data (pd.DataFrame): Long-form data.
        formulae (list): List of patsy-style formulae.

    """
    a = ['subj', 'M']
    b = ['D', 'S', 'H', 'F']
    terms = set(c for f in formulae for c in data.columns if c in f)
    data = pd.pivot_table(
        data, index=terms | set(a), aggfunc=np.sum
    ).reset_index()

    return data[a + list(terms) + b]


def dmforoffsets(data):
    """Create a design matrix for the offset variables (deltas)."""

    terms = (c for c in data.columns if c not in ['M', 'D', 'S', 'H', 'F'])
    formula = '0+' + ':'.join('C(%s)' % t for t in terms)

    return dmatrix(formula, data)

if __name__ == '__main__':

    data = get_toy_data()
    formulae = ['kappa ~ C(colour)', 'gamma ~ 1', 'zeta ~ 1']
    data = pivot(data, formulae)
    print(dmforoffsets(data))

