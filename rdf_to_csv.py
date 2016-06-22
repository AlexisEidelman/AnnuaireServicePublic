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

# certaines lignes ne semblent pas porter beaucoup d'informations
cols_remplies_seules = [
    'http://www.mondeca.com/system/basicontology#created_the',
    'http://www.mondeca.com/system/basicontology#updated_the',
    'http://www.mondeca.com/system/t3#bt',
    'http://www.mondeca.com/system/t3#nt',
    'http://www.w3.org/1999/02/22-rdf-syntax-ns#type',
    ]
sans_info = tab.drop(cols_remplies_seules, axis=1)
sans_info.dropna(how='all', inplace=True)
# c'est des assoc ?

tab = tab[tab.index.isin(sans_info.index)]
# 7336 lignes

tab.to_csv('AnnuaireServicePublic.csv')
