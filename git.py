# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 15:13:07 2016

@author: aeidelman
"""

import os
import git

join = os.path.join

repo = git.Repo(os.getcwd())            
tree = repo.heads[0].commit.tree
index = repo.index


for file in os.listdir('json'):
    os.rename(join('json', file), join('json', 'annuaire.json'))
    index.add(['json/annuaire.json'])
    date = file[9:-5]
    index.commit('json ' + date)
    os.rename(join('json', 'annuaire.json'), join('json', file))
    

0