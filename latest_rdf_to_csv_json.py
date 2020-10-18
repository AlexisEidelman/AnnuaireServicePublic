#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 16:53:25 2020

@author: boulot
"""


import urllib
import zipfile
from annuaire.get_data.rdf_extraction import rdf_extraction
from annuaire.get_data.download import (
    read_list_of_tables, _get_version, downalod_zip, extract_file)
from annuaire.config_annuaire import path


# actuel
url_path_ = 'https://echanges.dila.gouv.fr/OPENDATA/RefOrgaAdminEtat/FluxAnneeCourante/dila_refOrga_admin_Etat_fr_latest.zip'
dest_path = 'data/latest.zip'


data = urllib.request.urlopen(url_path_)
with open(dest_path, 'wb') as f:
    f.write(data.read())

tar = zipfile.ZipFile(dest_path)
tar.extractall('data/')
filename = tar.filelist[0].filename

rdf_extraction('data/' + filename,
               path_csv = 'data/latest.csv',
               path_json = 'data/latest.json')

