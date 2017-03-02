# -*- coding: utf-8 -*-
"""
@author: aeidelman
"""

import os
import pandas as pd

path = '/home/sgmap/data/SIRENE'

# avantage
path_file = os.path.join(path, 
                         'sirc-266_266_13705_201606_L_P_20161010_121909418-secondtry.csv')

tab = pd.read_csv(path_file, sep=';', nrows=100000,
                  encoding='cp1252', #iso-8859-15
#                 usecols = categorical_vars + ['avant_montant_ttc']
                 )

assert all(tab.APET700.str.len() == 5)

# public = tab[tab['NJ'].astype(str).str[0] == '7']
# print(len(public))

     
#av['year'] = av['avant_date_signature'].str[6:]
iter_csv = pd.read_csv(path_file,  sep=';',
                       encoding='cp1252',
                       iterator=True, 
                       chunksize=100000)

df = pd.concat([tab[tab['NJ'].astype(str).str[0].isin(['4','7'])]
    for tab in iter_csv])

path_output = os.path.join(path, 'sirene_NJ_4_et_7.csv')
df.to_csv(path_output,  sep=';',
                       encoding='cp1252',
                       iterator=True, 
                       index=False)