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

tab = pd.read_csv(path_file, sep=';', nrows=1000,
                  encoding='cp1252'
#                 usecols = categorical_vars + ['avant_montant_ttc']
                 )

assert all(tab.APET700.str.len() == 5)
public = tab[tab.APET700.str[:2] == '84']
print(len(public))

xxx
     
#av['year'] = av['avant_date_signature'].str[6:]
iter_csv = pd.read_csv(path_file,  sep=';',
                       encoding='cp1252',
                       iterator=True, 
                       chunksize=100000)

df = pd.concat([tab[tab.APET700.str[:2] == '84'] 
    for tab in iter_csv])

path_output = os.path.join(path, 'sirene84.csv')
df.to_csv(path_output,  sep=';',
                       encoding='cp1252',
                       iterator=True, 
                       index=False)