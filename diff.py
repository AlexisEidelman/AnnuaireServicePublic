# -*- coding: utf-8 -*-
"""
@author: Alexis Eidelman

Etudie les differences d'une version de l'annuaire à l'autre

TODO: retirer les updates_the de l'analyse, ils redondent
"""

import os
import pandas as pd

files = os.listdir('csv')
files.sort()

name1, name2 = files[:2]

def load(name):
    file = os.path.join('csv', name)
    tab = pd.read_csv(file)
    return tab



def diff_csv(name1, name2, verbose=True):
    ''' effectue la différence des deux csv
        retourne les lignes pour lesquelles les informations 
        dans '''
    tab1 = load(name1)
    tab2 = load(name2)
    
    merge = tab1.merge(tab2, on = ['index', 'parent'],
                   indicator=True, how='outer')
    
    if verbose:
        print(merge._merge.value_counts())

    cols_x = [col for col in merge.columns if col[-2:] == '_x']
    cols_y = [col for col in merge.columns if col[-2:] == '_y']

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
    return diff[['index', 'parent'] + cols_x]


def revient_a_la_valeur_initiale(name1, name2, name3):
    ''' regarde si les valeurs sont les mêmes dans name1 et name3 alors 
    qu'elles sont différentes dans name2
    '''
    tab1 = load(name1)
    tab2 = load(name2)
    tab3 = load(name2)
    
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
    test = revient_a_la_valeur_initiale('annuaire_20161019.csv',
                                        'annuaire_20161026.csv',
                                        'annuaire_20161102.csv')
    
    differents1 = diff_csv('annuaire_20161022.csv', 'annuaire_20161026.csv')
    differents2 = diff_csv('annuaire_20161026.csv', 'annuaire_20161102.csv')
    differents3 = diff_csv('annuaire_20161022.csv', 'annuaire_20161102.csv')

    for col in differents1.columns:
            if differents1[col].nunique() > 1:
                print(differents1[col].value_counts())
                print(differents2[col].value_counts())
                print('\n')
        
        
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