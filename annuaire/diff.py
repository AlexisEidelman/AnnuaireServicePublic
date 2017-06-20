# -*- coding: utf-8 -*-
"""
@author: Alexis Eidelman

Etudie les differences d'une version de l'annuaire à l'autre

TODO: retirer les updates_the de l'analyse, ils redondent
"""

import os
import pandas as pd

from load import load_csv
from annuaire.config_annuaire import path

def diff_csv(name1, name2, verbose=True, keep=None, drop=None):
    ''' effectue la différence des deux csv
        retourne les lignes pour lesquelles les informations 
        dans '''
    tab1 = load_csv(name1, drop, keep)
    tab2 = load_csv(name2, drop, keep)
    
    merge_on = ['index']
    merge = tab1.merge(tab2, on = merge_on,
                   indicator=True, how='outer',
                   suffixes=('_old','_new'))
    
    
    if verbose:
        print("Entre {} et {}, il y a {} nouvelles entrées et {} sorties".format(
                name1, name2, sum(merge._merge == 'right_only'),
                sum(merge._merge == 'left_only')))
        print(merge._merge.value_counts())

    cols_x = [col for col in merge.columns if col[-2:] == '_old']
    cols_y = [col for col in merge.columns if col[-2:] == '_new']

    merge_y = merge[cols_y].rename(columns=dict(x for x in zip(cols_y, cols_x)))
    similar = merge[cols_x] == merge_y 
    differents = ~similar.all(axis=1)
    if verbose:
        print("il y a {} differences sur {} entités".format(
            sum(differents),
            len(merge))
            )
    
    if verbose:
        print((~similar).sum())
    
    diff = merge[differents]
    diff[cols_x] = diff[cols_x].mask(similar)
    diff[cols_y] = diff[cols_y].mask(similar)
    diff[cols_x] += ' -> ' + merge_y[differents]
    return diff[merge_on + cols_x + ['_merge']]


def revient_a_la_valeur_initiale(name1, name2, name3, keep=None, drop=None):
    ''' regarde si les valeurs sont les mêmes dans name1 et name3 alors 
    qu'elles sont différentes dans name2
    '''
    tab1 = load_csv(name1, drop, keep)
    tab2 = load_csv(name2, drop, keep)
    tab3 = load_csv(name2, drop, keep)
    
    merge = tab1.merge(tab2, on = ['index', 'parent']). \
        merge(tab3, on = ['index', 'parent'])
    

    cols_x = [col for col in merge.columns if col[-2:] == '_x']
    cols_y = [col for col in merge.columns if col[-2:] == '_y']
    cols_z = [col[:-2] for col in cols_x ]
    
    merge_y = merge[cols_y].rename(columns=dict(x for x in zip(cols_y, cols_x)))
    merge_z = merge[cols_z].rename(columns=dict(x for x in zip(cols_z, cols_x)))    
    similar_x_z = merge[cols_x] == merge_z 
    different_x_y = merge[cols_x] != merge_y
    similar_y_z = merge_y == merge_z
    return similar_x_z & different_x_y
#matchees = merge[merge._merge == 'both']
#del matchees['_merge']
#
#matchees.fillna('nan', inplace=True)
#
#            
#return differents

if __name__ == '__main__':
#    test = revient_a_la_valeur_initiale('annuaire_20161019.csv',
#                                        'annuaire_20161022.csv',
#                                        'annuaire_20161026.csv')
#                                        
    path_csv = path['csv']
    name1 = os.listdir(path_csv)[0]
    name2 = os.listdir(path_csv)[1]
    
    basic_drop =  ['http://www.mondeca.com/system/basicontology#updated_the',
                   'an/telecopie', 'an/telephone'] 
    keep_for_sirene = ['index', 'parent',
                       'an/adressePhysiqueCodePostal',
                       'an/adressePhysiqueVille',
                       'http://www.w3.org/2000/01/rdf-schema#label',
                       ]                            
    differents1 = diff_csv(name1, name2, keep=keep_for_sirene)
    differents2 = diff_csv('annuaire_20161026.csv', 'annuaire_20161102.csv',
                            keep=keep_for_sirene)
    differents3 = diff_csv('annuaire_20161022.csv', 'annuaire_20161102.csv',
                            keep=keep_for_sirene)

#    for col in differents3.columns:
#            if differents1[col].nunique() > 5:
#                print(differents1[col].value_counts().head())
#                print(differents2[col].value_counts().head())
#                print('\n')
#                
#    for tab in [differents1, differents2, differents3]:
#        print('en tout on a {} changement'.format(len(tab)))        
#        changements = tab.notnull().sum()
#        changements.drop(['parent', 'index'], inplace=True)        
#        changements.sort_values(ascending=False, inplace=True)
#        print(changements.head(7))
    
    diff_6_mois = diff_csv('annuaire_20160702.csv', 'annuaire_20161112.csv',
                            keep=keep_for_sirene)
    both = diff_6_mois[diff_6_mois._merge == 'both']
    diff_label = both2['http://www.w3.org/2000/01/rdf-schema#label_x']
    diff_label = diff_label[diff_label.notnull()]
    
    result = ''              
    for changement in diff_label.values:
        chgt = changement
        chgt = chgt.replace('->','\n \t devient \n')
        result += chgt + '\n --- \n'

    with open('chgt_noms_matcheds.txt', 'w') as f:
        f.write(result)

#Il y a des choses étonnantes dans les adresses des sites web par exemple. 
#http://www.defense.gouv.fr/dga -> http://www.ixarm.com                           39
#http://www.education.gouv.fr -> http://www.enseignementsup-recherche.gouv.fr     37
#http://www.enseignementsup-recherche.gouv.fr -> http://www.education.gouv.fr     35
#http://www.ixarm.com -> http://www.defense.gouv.fr/dga                           31
#
#http://www.education.gouv.fr -> http://www.enseignementsup-recherche.gouv.fr          40
#http://www.ixarm.com -> http://www.defense.gouv.fr/dga                                38
#http://www.defense.gouv.fr/dga -> http://www.ixarm.com                                35
#http://www.enseignementsup-recherche.gouv.fr -> http://www.education.gouv.fr          34