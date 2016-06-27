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


g = rdflib.Graph()
g.parse('annuaire_gouv.rdf', format='xml')


def load_all():
    DF = rdflib.Namespace('http://www.df.gouv.fr/administration_francaise/annuaire#')
    requete =  g.query("""SELECT ?a ?b ?c
        WHERE {?a ?b ?c }""", 
        initNs={ 'df': DF })
    return requete
data = load_all()

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

tab = pd.DataFrame.from_dict(diction).T
# 13877 lignes
# 50 colonnes = 50 prédicats différents


# il y a 3 doublons : tab.duplicated().sum()
tab.drop_duplicates(inplace=True)

## propriété de la table
tab.isnull().sum()
for col in tab.columns:
    print(tab[col].value_counts().head(3))

# certaines lignes correspondent à des associations :
# liens entre les entité
cols_remplies_seules = [
    'http://www.mondeca.com/system/basicontology#created_the',
    'http://www.mondeca.com/system/basicontology#updated_the',
    'http://www.mondeca.com/system/t3#bt',
    'http://www.mondeca.com/system/t3#nt',
    'http://www.w3.org/1999/02/22-rdf-syntax-ns#type',
    ]
# en gros, bt, c'est l'enfant et nt c'est le parent

sans_liens = tab.drop(cols_remplies_seules, axis=1)
sans_liens.dropna(how='all', inplace=True)
# tab.loc[tab.index.isin(sans_liens.index), cols_remplies_seules].notnull().sum()
entites = tab.loc[tab.index.isin(sans_liens.index)].drop(
    ['http://www.mondeca.com/system/t3#bt', 'http://www.mondeca.com/system/t3#nt'
    ], axis=1)
# entites['http://www.w3.org/1999/02/22-rdf-syntax-ns#type'].value_counts()
# => on a plusieurs types
# 7336 lignes

assoc = tab.loc[~tab.index.isin(sans_liens.index), cols_remplies_seules]
# assoc['http://www.w3.org/1999/02/22-rdf-syntax-ns#type'].value_counts()
# => on n'a qu'un seul type
del assoc['http://www.w3.org/1999/02/22-rdf-syntax-ns#type']
# 6538 lignes

joined = entites.reset_index().merge(assoc, #left_index=True, 
                       left_on='index',
                       right_on='http://www.mondeca.com/system/t3#nt',
                       how='left')

joined['http://www.mondeca.com/system/t3#bt'].value_counts(dropna=False)
joined[joined['http://www.mondeca.com/system/t3#bt'].isnull()]

joined.columns = joined.columns.tolist()[:-2] + ['parent', 'id']
# (joined['index'] == joined['id'])[joined['id'].notnull()].all() is True
del joined['id']

# on peut probablement retirer ces éléments :
joined = joined[~joined['index'].str.contains('df')]

### 


joined['parent'].fillna('source', inplace=True)
variables_fiche = ['http://www.w3.org/2000/01/rdf-schema#label',
                   'df/sigle']


# Utilisation de NetworkX
import networkx as nx
G=nx.Graph()
                   
usefull = joined[variables_fiche + ['parent', 'index']]
usefull.columns = ['label', 'sigle', 'parent', 'index']

usefull['sigle'].fillna('nc.', inplace=True)
usefull['label'].fillna('nc.', inplace=True)

G = nx.from_pandas_dataframe(
    usefull, 
    'parent', 'index', ['label', 'sigle'],
    nx.DiGraph()
    )


def recursive_run(item, dico_values):
    children = [recursive_run(el, G[item][el]) 
                for el in G.successors_iter(item)]
    dico_values['name'] = item
    if len(children) != 0:
        dico_values['children'] = children
    return dico_values


tree = recursive_run('source', dict())
import json
with open('data3.json', 'w') as outfile:
    json.dump(tree, outfile, indent=2, sort_keys=True)


joined.to_csv('AnnuaireServicePublic.csv', index=False)
