import urllib.request
import numpy as np
import pandas as pd
from itertools import product
from patsy import dmatrix


def get_rouder_data():
    """Download the Rouder et al. data. Requires internet access.

    Returns:
        pd.DataFrame: Rouder et al. data.

    """

    data = pd.read_csv(urllib.request.urlopen(
        'https://raw.githubusercontent.com/PerceptionCognitionLab/data0/' +
        'master/wmPNAS2008/lk2clean.csv'
    ))
    data = data[['sub', 'prch', 'N', 'ischange', 'resp', 'oldcol']]
    data['subject'] = data['sub']
    data['prob_different'] = data.prch
    data['colour'] = data.oldcol
    data['set_size'] = data.N
    data['different_trials'] = data.ischange
    data['same_trials'] = (1 - data.ischange)
    data['hits'] = data.ischange * data.resp
    data['false_alarms'] = (1 - data.ischange) * data.resp
    data = data[
        ['subject', 'prob_different', 'colour', 'set_size', 'different_trials',
         'same_trials', 'hits', 'false_alarms']]
    return data


def compress(data, formulae):
    """Compress the data frame so that all trials belonging to a unique
    condition are represented by a single row in the data frame. It is safe to
    apply this to a data frame more than once.

    Args:
        data (pd.DataFrame): Long-form data.
        formulae (list): List of patsy-style formula.

    Returns:
        pd.DataFrame: Compressed data.

    """
    a = ['subject']
    b = ['set_size', 'different_trials', 'same_trials', 'hits', 'false_alarms']
    terms = [c for f in formulae for c in data.columns if
             c not in a + b and c in f]
    data = pd.pivot_table(data, index=a + terms + b[:1], aggfunc=np.sum)
    data = data.drop([c for c in data.columns if c not in a + b + terms],
                     axis=1).reset_index()
    cartesian = product(data.columns.tolist(), data.columns.tolist())
    ok = all((x not in y) for x, y in cartesian if x != y)
    assert ok, 'The name of an independent variable is a subset of another.'
    return data[a + list(terms) + b]


def dm_for_lower_stochastics(data):
    """Every subject/condition combination needs its own stochastic node.
    Usually this would be trivial to implement, because that would be each row
    in the data frame. Unfortunately for working-memory tasks this is not the
    case, because subjects are presented with multiple set sizes per condition.
    We DON'T want a stochastic node for every set size. I think that the most
    efficient way to implement this is to create a vector of offset variables
    and pair them to the correct rows using a new design matrix. This should
    deal with imbalances in the data (e.g., if not every subject was tested
    with every set size per condition).

    Args:
        data (pd.DataFrame): Compressed data.

    Returns:
        patsy.dmatrix: Design matrix.

    """

    not_these = ['set_size', 'different_trials', 'same_trials', 'hits',
                 'false_alarms']
    terms = [c for c in data.columns if c not in not_these]
    formula = '0+' + ':'.join('C(%s)' % t for t in terms)
    return dmatrix(formula, data)

