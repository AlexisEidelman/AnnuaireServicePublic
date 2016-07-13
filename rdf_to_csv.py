# -*- coding: utf-8 -*-
"""
@author: Alexis Eidelman

Travaille sur les données issues de 
https://www.data.gouv.fr/fr/datasets/
service-public-fr-annuaire-de-ladministration-base-de-donnees-nationales/

pour obtenir le graph des administrations
Il y a 223874 triplets
7336 entités

"""

import rdflib
import pandas as pd

def all_triplets():
    ''' la requete de tous les triplets '''
    DF = rdflib.Namespace('http://www.df.gouv.fr/administration_francaise/annuaire#')
    requete =  g.query("""SELECT ?a ?b ?c
        WHERE {?a ?b ?c }""", 
        initNs={ 'df': DF })
    return requete


def triplets_to_dict(data):
    # pour simplifier l'écriture
    df = 'http://www.df.gouv.fr/administration_francaise/annuaire#'
    ann = 'http://lannuaire.service-public.fr/'
    # crée un dictionnaire 
    diction = dict()
    for row in data:
        index = row[0].toPython()
        index = index.replace(df, 'df/').replace(ann, 'an/')
        predicat = row[1].toPython().replace(df, 'df/').replace(ann, 'an/')
        attribut = row[2].toPython()
        if isinstance(attribut, str):
            attribut = attribut.replace(df, 'df/').replace(ann, 'an/')
        if index not in diction:
            diction[index] = dict()
        diction[index][predicat] = attribut
    return diction


def _notnull_columns(tab):
    ''' retourne les variables qui ont des 
    valeurs non nulles '''
    nb_notnull = tab.notnull().sum()
    cols_notnull = nb_notnull[nb_notnull > 0]
    return cols_notnull.index.tolist()


def _only_notnull_columns(tab):
    ''' table sans les colonnes entierement nulles '''
    return tab[_notnull_columns(tab)]


g = rdflib.Graph()
g.parse('annuaire_gouv.rdf', format='xml')
data = all_triplets()
diction = triplets_to_dict(data)
tab = pd.DataFrame.from_dict(diction).T
# 13877 lignes
# 50 colonnes = 50 prédicats différents

# il y a 3 doublons : tab.duplicated().sum()
tab.drop_duplicates(inplace=True)

## propriété de la table
tab.isnull().sum()
for col in tab.columns:
    print(tab[col].value_counts().head(3))


def find_association(tab):
    type_ = tab["http://www.w3.org/1999/02/22-rdf-syntax-ns#type"]

    # certaines lignes correspondent à des associations :
    # liens entre les entité
    association = tab[type_ == 'http://www.mondeca.com/system/t3#BN']    
    association = _only_notnull_columns(association)
    # en gros, nt, Narrower Term c'est l'enfant
    # bt, Broader Term, c'est le parent
    association.rename(columns={
        'http://www.mondeca.com/system/t3#bt': 'parent',
        'http://www.mondeca.com/system/t3#nt': 'enfant',
        },
        inplace=True)
    
    AutreHierarchie = tab[type_ == 'df/AutreHierarchie']
    AutreHierarchie = _only_notnull_columns(AutreHierarchie)
    AutreHierarchie.rename(columns={
        'df/serviceFils': 'enfant',
        'df/servicePere': 'parent',
        },
        inplace=True)    
    
    return AutreHierarchie.append(association)   
    #    # ancienne version
    #        cols_association = [
    #            'http://www.mondeca.com/system/basicontology#created_the',
    #            'http://www.mondeca.com/system/basicontology#updated_the',
    #            'http://www.mondeca.com/system/t3#bt',
    #            'http://www.mondeca.com/system/t3#nt',
    #            'http://www.w3.org/1999/02/22-rdf-syntax-ns#type',
    #            ]
    #        # en gros, bt, c'est l'enfant et nt c'est le parent
    #        
    #        sans_liens = tab.drop(cols_association, axis=1)
    #        sans_liens.dropna(how='all', inplace=True)
    #        # tab.loc[tab.index.isin(sans_liens.index), cols_remplies_seules].notnull().sum()
    #        entites = tab.loc[tab.index.isin(sans_liens.index)].drop(
    #            ['http://www.mondeca.com/system/t3#bt', 'http://www.mondeca.com/system/t3#nt'
    #            ], axis=1)
    #        # entites['http://www.w3.org/1999/02/22-rdf-syntax-ns#type'].value_counts()
    #        # => on a plusieurs types
    #        # 7336 lignes
    #        
    #        assoc = tab.loc[~tab.index.isin(sans_liens.index), cols_association]
    #        # assoc['http://www.w3.org/1999/02/22-rdf-syntax-ns#type'].value_counts()
    #        # => on n'a qu'un seul type
    #        del assoc['http://www.w3.org/1999/02/22-rdf-syntax-ns#type']
    #        # 6538 lignes
    # return association

assoc = find_association(tab)

entites = assoc['enfant'].tolist() + assoc['parent'].tolist()

# on ne garde que certain types peut probablement retirer ces éléments :
type_entity = tab["http://www.w3.org/1999/02/22-rdf-syntax-ns#type"]
list_types = ['an/ServiceRAF'] # 'df/AutreHierarchie']
tab1 = tab[type_entity == 'an/ServiceRAF']

tab_avec_liens = tab1.reset_index().merge(assoc, #left_index=True, 
    left_on='index',
    right_on='enfant',
    how='left',
    suffixes=('','_lien'),
    indicator=True)

#, 'df/Ministere',
# à df/ministère correspondent les département et des entités
# qui existe par ailleurs. On peu supprimer
# qui sont le 13 qui n'ont pas de parent ?
tab_avec_liens[tab_avec_liens._merge == 'left_only']

# TODO: gérer les autres hiérarchie

# TODO: regarde les départements
tab_avec_liens[type_entity == 'df/Ministere']
joined = tab_avec_liens
joined[type_entity == 'df/Ministere'].notnull().sum()
joined[joined['index'] == "itm:n#_180995"]

joined = joined[~joined['http://www.w3.org/2000/01/rdf-schema#label'].str.contains('<< Dép.')]
# => on retire 101 lignes






# Utilisation de NetworkX
import networkx as nx
G=nx.Graph()

variables_fiche = ['http://www.w3.org/2000/01/rdf-schema#label',
                   'df/sigle']
tab_avec_liens['parent'].fillna('source', inplace=True)
usefull = tab_avec_liens[variables_fiche + ['parent', 'index']]
usefull.columns = ['label', 'sigle', 'parent', 'index']

usefull['sigle'].fillna('nc.', inplace=True)
usefull['label'].fillna('nc.', inplace=True)

G = nx.from_pandas_dataframe(
    usefull, 
    'parent', 'index', ['label', 'sigle'],
    nx.DiGraph()
    )


def recursive_run(G, item, dico_values):
    children = [recursive_run(G, el, G[item][el]) 
                for el in G.successors_iter(item)]
    dico_values['name'] = item
    if len(children) != 0:
        dico_values['children'] = children
    return dico_values

tree = recursive_run(G, 'source', dict())
tree['label'] = 'source'
import json
with open('data.json', 'w') as outfile:
    json.dump(tree, outfile, indent=2, sort_keys=True)


tab_avec_liens.to_csv('AnnuaireServicePublic.csv', index=False)
