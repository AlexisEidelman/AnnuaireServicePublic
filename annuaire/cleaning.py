#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 18:33:57 2017

@author: sgmap
"""
import os
import pandas as pd

from load import load_csv

def clean_sigle():
    # cf ci-dessous
    pass

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