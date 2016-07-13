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
import tarfile

url_path = 'https://lecomarquage.service-public.fr/annuaire_institutionnel/'

def read_list_of_tables(url_path):
    ''' charge l'url, et sort tous 
        les éléments a avec href '''
    html = urllib.request.urlopen(url_path)
    html_page = html.read()
    
    soup = BeautifulSoup(html_page, "lxml")
    #le parsing est basique mais efficace pour l'instant
    files = []
    for link in soup.findAll('a'):
        files.append(link.get('href'))    
    return files

files = read_list_of_tables(url_path)
files.remove('export_data_gouv_latest.tar.bz2')
files.remove('../')

def downalod_zip(url_path, file):
    dest_path = os.path.join('zip', file)
    if not os.path.exists(dest_path):
        url = urllib.parse.urljoin(url_path, file)
        data = urllib.request.urlopen(url)
        with open(dest_path, 'wb') as f:
            f.write(data.read())

def extract_file(file):
    ''' extrait le fichier et le renomme '''
    new_name = os.path.join('data',
                             'annuaire_' + file[17:25] + '.rdf')
    if not os.path.exists(new_name):                       
        dest_path = os.path.join('zip', file)
        tar = tarfile.open(dest_path, "r:bz2")
        tar.extractall('data')
        old_name = os.path.join('data',
                                 'export_data_gouv.rdf')
        os.rename(old_name, new_name)
    
for file in files:
    downalod_zip(url_path, file)
    extract_file(file)
    

