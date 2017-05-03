# -*- coding: utf-8 -*-
"""
Created on Mon May 30 14:12:54 2016

Travaille sur les données issues de 
https://www.data.gouv.fr/fr/datasets/
service-public-fr-annuaire-de-ladministration-base-de-donnees-nationales/

pour obtenir le graph des administrations
Il y a 223874 triplets
7252 entité

@author: aeidelman
"""
import os
import urllib
from bs4 import BeautifulSoup
import zipfile

url_path = 'https://echanges.dila.gouv.fr/OPENDATA/RefOrgaAdminEtat/FluxHistorique/2017-FluxCourant'

def _get_version(filename):
    return file[-12:-4]

def read_list_of_tables(url_path):
    ''' charge l'url, et sort tous 
        les éléments a avec href 

        Note le site de la dila exige désormais un niveau de sécurité SSL
        compatible seulement avec la version 3.5.3 et supérieur de python
        '''
    html = urllib.request.urlopen(url_path)
    html_page = html.read()
    
    soup = BeautifulSoup(html_page, "lxml")
    #le parsing est basique mais efficace pour l'instant
    files = []
    for link in soup.findAll('a'):
        files.append(link.get('href'))

    return files

files = read_list_of_tables(url_path)
files = [x for x in files if x is not None and 'latest' not in x]
files.remove('#index')

def downalod_zip(url_path, file):
    dest_path = os.path.join('zip', _get_version(file) + '.zip')
    if not os.path.exists(dest_path):
        url = urllib.parse.urljoin(url_path, file)
        data = urllib.request.urlopen(url)
        with open(dest_path, 'wb') as f:
            f.write(data.read())

def extract_file(file):
    ''' extrait le fichier et le renomme '''
    new_name = os.path.join('data',
                             _get_version(file) + '.rdf')
    if not os.path.exists(new_name):                       
        dest_path = os.path.join('zip', file[-12:])
        tar = zipfile.ZipFile(dest_path)
        tar.extractall('data')
        old_name = os.path.join('data',
                                 os.path.basename(file)[:-4] + '.rdf')
        os.rename(old_name, new_name)

for file in files:
    downalod_zip(url_path, file)
    extract_file(file)
    

