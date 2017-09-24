# -*- coding: utf-8 -*-
"""
@author: aeidelman
"""

import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import pandas as pd
import load

annuaire = load.load_csv('annuaire_20160702.csv', 
    keep=['index','df/competences',
          'df/competenceGeographique',
          'df/ministereDeRattachement', 
          'http://www.w3.org/2000/01/rdf-schema#label',
          'parent',
          'an/adressePhysiqueCodePostal',
          'an/adressePhysiqueVille',
          ]
    )


from read_extract import public

# on cherche sur un cas : le conseil supérieur de la magistrature
public.iloc[43]['NOMEN_LONG']

label = annuaire['http://www.w3.org/2000/01/rdf-schema#label']
cond1 = label.str.contains('agistr') & label.str.contains('onseil')
label[cond1].iloc[0]

public['NOMEN_LONG'] = public['NOMEN_LONG'].str.lower()

nom_a_exclure = ['commune', 'communal', 'sncf', 'pole emploi',
                 'ctre com action sociale']
for nom in nom_a_exclure:
    public = public[~public['NOMEN_LONG'].str.contains(nom)]

public['NOMEN_LONG'] = public['NOMEN_LONG'].str.replace('ctre', 'centre')
public['NOMEN_LONG'] = public['NOMEN_LONG'].str.replace('nat ', 'national ')
public['NOMEN_LONG'] = public['NOMEN_LONG'].str.replace('univ ', 'universitaires et ')


annuaire['label'] = label.str.lower()
annuaire['label'] = annuaire['label'].str.replace('é','e')
annuaire['label'] = annuaire['label'].str.replace('ç','c')
annuaire['label'] = annuaire['label'].str.split(' \(').str[0]

selected_NJ = [4110, 4120, 4140, 4150,
               7111, 7112, 7130, 7160,
               7379, 7381, 7382, 7384, 
               7389,
               7410,
               ]
               
merge = pd.merge(annuaire, public[public['NJ'].isin(selected_NJ)],
                 right_on = 'NOMEN_LONG',
                 left_on = 'label',
                 indicator=True,
                 how='outer',
                 )
                 
merge._merge.value_counts()
matched = merge[merge._merge == 'both']


# un exemple de mauvais merge
merge[merge._merge == 'left_only']['label'].value_counts()
merge[merge._merge == 'right_only']['NOMEN_LONG'].value_counts().head()
right = merge[merge._merge == 'right_only']

merge[merge._merge == 'left_only']['label'].value_counts()
secretariat = merge[merge.label == 'secretariat general']
sum(public.NOMEN_LONG.str.contains('secretariat gene'))

ANTS = public.SIREN == 130003262
public[ANTS].NOMEN_LONG

SAN = annuaire['label'] == "service agence du numerique"
SAN = annuaire[SAN]
sum(public['NOMEN_LONG'] == "service agence du numerique")
SAN_SIREN = public.NOMEN_LONG.str.contains('numerique')

SAN_SIREN = public.NOMEN_LONG == "secretariat d'etat charge du numerique".lower()
sum(public.SIREN == 110000379)

public[public.SIREN == 110002011]