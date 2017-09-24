#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 18:33:57 2017

@author: sgmap
"""
import os
import numpy as np
import pandas as pd

from annuaire.load import load_csv

def clean_sigle(table_ini):
    table = table_ini.copy()
    label = 'http://www.w3.org/2000/01/rdf-schema#label'
    # sigle2 : les termes entre parenthèses de label qui commence par 2 majuscules
    sigle2 = table[label].str.extract("\(([A-Z][A-Z].*?)\)")
    table['sigle2'] = sigle2
    table['nom_sans_sigle'] = table[label].str.split('\(').str[0]

    # une colonne unique
    for idx, row in table[['df/sigle','sigle2']].iterrows():
        if row['sigle2'] not in [np.nan, 'nc.']:
            if row['df/sigle'] != 'nc.':
                if row['sigle2'] != row['df/sigle']:
                    print(row)
    
    cond = (table['df/sigle'] != 'nc.')  & (table['sigle2'].isnull())
    table.loc[cond, 'sigle2'] = table.loc[cond, 'df/sigle']
    
    return table

if __name__ == '__main__':

    tab1 = load_csv('20170610.csv')
    sigle1 = tab1['df/sigle']
    label = 'http://www.w3.org/2000/01/rdf-schema#label'
    # sigle2 : les termes entre parenthèses de label qui commence par 2 majuscules
    sigle2 = tab1[label].str.extract("\(([A-Z][A-Z].*?)\)")

    # Remarque: pour être plus propre, on pourrait regarder les deux valeurs issues de
#    sigle2 = tab1[label].str.extractall("\(([A-Z][A-Z].*?)\)")
#    sigle2 = sigle2.reset_index()
#    sigle2['match'].value_counts()
#    sigle2[sigle2['match'] == 1]
    tab1.loc[[519,3567], label]
    
    sigle2.fillna("nc.") == sigle1
    
    test = clean_sigle(tab1)
    