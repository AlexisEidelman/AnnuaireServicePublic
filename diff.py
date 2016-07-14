# -*- coding: utf-8 -*-
"""
@author: Alexis Eidelman

Etudie les differences d'une version de l'annuaire à l'autre

"""

import os
import pandas as pd

files = os.listdir('csv')
files.sort()

name1, name2 = files[:2]

def load(name):
    file = os.path.join('csv', name)
    tab = pd.read_csv(file)
    tab.drop('_merge', axis=1, inplace=True)
    return tab

tab1 = load(name1)
tab2 = load(name2)

merge = tab1.merge(tab2, on = ['index', 'parent'],
                   indicator=True, how='outer')
        
merge._merge.value_counts()

diff1 = merge[merge._merge != 'both']

matchees = merge[merge._merge == 'both']
cols_1 = [col for col in matchees.columns if col[-2:] == '_x']

del matchees['_merge']
matchees.fillna('nan', inplace=True)
for col in cols_1:
    nb_diff = sum(matchees[col] != matchees[col[:-1] + 'y'])
    if nb_diff > 0:
        print(col)
        print(nb_diff)