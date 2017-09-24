# -*- coding: utf-8 -*-
"""
@author: aeidelman
"""

import os
import pandas as pd

path = '/home/sgmap/data/SIRENE'

path_extract = os.path.join(path, 'sirene_NJ_4_et_7.csv')

tab = pd.read_csv(path_extract,
                  sep=';',
                  encoding='cp1252'
                  )

print(tab.SIREN.value_counts())


##  inspect data

def clean_empty_col(tab):
    notnull = tab.notnull().sum()
    allnull = notnull[notnull == 0].index
    return tab.drop(allnull, axis=1)


def clean_unique_value_col(tab):
    unique_value_cols = list()    
    for col in tab.columns:
        if tab[col].nunique() == 1:
            unique_value_cols += [col]
            print('La colonne {} a une seule valeur : {}'.format(
                col, tab[col].iloc[0]))
    return tab.drop(unique_value_cols, axis=1)


def how_many_values(tab):
    tab = clean_empty_col(tab)
    for col in tab.columns:
        if tab[col].nunique() < 5:
            print(tab[col].value_counts())


nom_SIREN = tab.groupby(['SIREN', 'NOMEN_LONG']).size()
# quelques questions sur des SIREN a plusieurs noms.
nom_SIREN[nom_SIREN != 1]

tab_130005481 = tab[tab.SIREN == 130005481]

public = clean_empty_col(tab)
public = clean_unique_value_col(public)