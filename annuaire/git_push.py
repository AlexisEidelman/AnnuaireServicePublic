# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 15:13:07 2016

@author: aeidelman
"""

import os
import git

from annuaire.config_annuaire import path

join = os.path.join

repo = git.Repo(os.getcwd())            
tree = repo.heads[0].commit.tree
index = repo.index

past_commit_messages = [commit.message for commit in repo.iter_commits()]

files = os.listdir(path['json'])
files.sort()

for file in files:
    date = file[9:-5]
    name_commit = 'json ' + date
    if name_commit not in past_commit_messages:
        print(name_commit)
        os.rename(join(path['json'], file), join(path['json'], 'annuaire.json'))
        index.add(['json/annuaire.json'])
        index.commit('json ' + date)
        os.rename(join(path['json'], 'annuaire.json'), join(path['json'], file))
    
