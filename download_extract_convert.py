# -*- coding: utf-8 -*-
"""
@author: Alexis Eidelman

Prend tous les fichiers les télécharge et les transforme en 
csv et en json

"""

import os

from annuaire.rdf_extraction import rdf_extraction
from annuaire.download import (
    read_list_of_tables, _get_version, downalod_zip, extract_file)
from annuaire.config_annuaire import path

url_path = 'https://echanges.dila.gouv.fr/OPENDATA/RefOrgaAdminEtat/FluxHistorique/2017-FluxCourant'

files = read_list_of_tables(url_path)
files = [x for x in files if x is not None and 'latest' not in x]
files.remove('#index')

files_to_download = [x for x in files 
    if _get_version(x) + '.rdf' not in os.listdir(path['data'])
    ]
        
for file in files:
    downalod_zip(url_path, file)
    extract_file(file)
    
files = os.listdir(path['data'])
names = [file[:-4] for file in files]

for name in names:
    csv_name = os.path.join(path['csv'], name + '.csv')
    json_name = os.path.join(path['json'], name + '.json')
    if not os.path.exists(csv_name) or not os.path.exists(json_name):
        rdf_extraction(name)