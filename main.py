# -*- coding: utf-8 -*-
"""
@author: Alexis Eidelman

Prend tous les fichiers téléchargés et les transforme en 
csv et en json

"""

import os

from rdf_extraction import rdf_extraction

files = os.listdir('data')
names = [file[:-4] for file in files]

for name in names:
    csv_name = os.path.join('csv', name + '.csv')
    json_name = os.path.join('json', name + '.json')
    if os.path.exists(csv_name) & os.path.exists(json_name):
        pass
    else:
        rdf_extraction(name)