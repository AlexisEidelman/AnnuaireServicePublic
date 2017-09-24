# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 18:29:54 2016

@author: aeidelman
"""

import os
import pandas as pd

from annuaire.config_annuaire import path

def load_csv(name, drop=None, keep=None):
    file = os.path.join(path['csv'], name)
    tab = pd.read_csv(file, encoding='utf8')
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


def load_num_csv(num):
    list_ = os.listdir(path['csv'])
    list_.sort()
    return load_csv(list_[num])
    

if __name__ == '__main__':
    files = os.listdir(path['csv'])
    files.sort()
    name1, name2 = files[:2]
    test1 = load_csv(name1)
    test2 = load_csv(name1, keep=['index','df/competences',
   'df/competenceGeographique',
   'df/ministereDeRattachement', 
   'http://www.w3.org/2000/01/rdf-schema#label',
   'parent']
   )