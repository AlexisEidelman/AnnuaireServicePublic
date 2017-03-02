# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 14:31:31 2016

@author: aeidelman
"""

import os
import json

files = os.listdir('json')
files.sort()
names = [file[:-4] for file in files]

for k in range(1,len(files) - 1):
    file1 = files[k]
    f = open('json/' + file1)
    v1 = json.load(f)
    
    file2 = files[k+1]
    f = open('json/' + file2)
    v2 = json.load(f)
    
    
    
    
    # difference de keys...
    set1 = set(v1)
    set2 = set(v2)
    dans2_pas_dans1 = set2 - set1
    dans1_pas_dans2 = set1 - set2
    
    # la différence entre tous les éléments
    differences = list()
    for entite in v1.keys():
        if entite in v2.keys():
            dict1 = v1[entite]
            dict2 = v2[entite]
            
            keys1 = set(dict1.keys())
            keys2 = set(dict2.keys())
            
            for champs in keys1 & keys2:
                value1 = dict1[champs]
                value2 = dict2[champs]
                if value2 != value1:
                    differences += [(entite, champs,
                                     value1, value2)]
            
            for champs in keys2 - keys1:
                differences += [(entite, champs,
                                     '', dict2[champs])]
    
            for champs in keys1 - keys2:
                differences += [(entite, champs,
                                     dict1[champs], '')]
            
    #import pdb
    #pdb.set_trace()
    
    # analyse des différences
    import pandas as pd
    diff_df = pd.DataFrame(differences)
    changes = diff_df[2] + '\n  devient \n  ' + diff_df[3]

    print(diff_df[0].value_counts().head())
    print(diff_df[1].value_counts())

    for row in changes.value_counts().head(10).items():
        print('On a {0} changements où \n {1} \n'.format(row[1], row[0]))
        
    un_pb = 'df/Ministeres_Ministere_de_l_economie_de_l_industrie_et_de_l_emploi'
    diff_df[diff_df[3] == un_pb]
    
    # inversions
    inversion = (diff_df[2] + diff_df[3]).isin(diff_df[3] + diff_df[2])
    
    
