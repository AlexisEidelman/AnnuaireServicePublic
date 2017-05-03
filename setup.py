# -*- coding: utf-8 -*-
"""

"""

from setuptools import setup, find_packages

import annuaire

import sys

if sys.version_info < (3,5,3):
    sys.exit('Pour télécharger les données automatiquement, il faut le ' + 
        'le programme SSL qui va avec Python 3.5.3')
    

setup(
    name = 'annuaire',
    version = '0.1.0.dev',
    url = 'https://github.com/AlexisEidelman/AnnuaireServicePublic.git',
    license = 'http://www.fsf.org/licensing/licenses/agpl-3.0.html',
    author='Alexis Eidelman',
    description="Utilisation et diff de l'organisation de l'État",
    packages=find_packages(), 
    zip_safe=False,
    platforms='any',
    install_requires=['pandas'],
    include_package_data=True,
)

