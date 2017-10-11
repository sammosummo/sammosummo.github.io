import urllib.request
import numpy as np
import pandas as pd


def get_toy_data():
    """Download and return the formatted Rouder PNAS data as a dataframe.

    """

    data = pd.read_csv(urllib.request.urlopen(
        'https://raw.githubusercontent.com/PerceptionCognitionLab/data0/' +
        'master/wmPNAS2008/lk2clean.csv'
    ))
    data = data[['sub', 'prch', 'N', 'ischange', 'resp', 'oldcol']]
    data['subj'] = data['sub']
    data['clr'] = data.oldcol
    data['M'] = data.N
    data['D'] = data.ischange
    data['H'] = data.ischange * data.resp
    data['S'] = (1 - data.ischange)
    data['F'] = (1 - data.ischange) * data.resp
    data = data[['subj', 'prch', 'clr', 'M', 'D', 'S', 'H', 'F']]

    return pd.pivot_table(
        data, index=['subj', 'prch', 'clr', 'M'], aggfunc=np.sum
    ).reset_index()


def fcn(s):
    """Nicely format a covariate name for LaTeX."""

    return '_{_\mathrm{' + ''.join(i for i in s if i not in "',") + '}}'


def formuale_list_to_dic(formulae, params):
    """Convert a list of formulae into a dic."""

    dic = {p: '1' for p in params}
    dic.update(
        {f.split('~')[0].replace(' ', ''): f.split('~')[1] for f in formulae}
    )

    return dic

if __name__ == '__main__':

    print(get_toy_data())
    print(formuale_list_to_dic(["k~c('subj')"]))
