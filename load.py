# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 18:29:54 2016

@author: aeidelman
"""

import os
import inspect
import pandas as pd

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

def load_csv(name, drop=None, keep=None):
    file = os.path.join(currentdir, 'csv', name)
    tab = pd.read_csv(file)
    if drop is not None:
        assert keep is None
        assert isinstance(drop, list)
        assert all([x in tab.columns for x in drop])
        to_keep = [x for x in tab.columns if x not in drop]
        tab = tab[to_keep]
    
    if keep is not None:
        assert drop is None
        assert isinstance(keep, list)
        assert all([x in tab.columns for x in keep])
        tab = tab[keep]
    
    return tab

if __name__ == '__main__':
    files = os.listdir('csv')
    files.sort()
    name1, name2 = files[:2]
    test1 = load_csv(name1)
    test2 = load_csv(name1, keep=['index','df/competences',
   'df/competenceGeographique',
   'df/ministereDeRattachement', 
   'http://www.w3.org/2000/01/rdf-schema#label',
   'parent']
   )