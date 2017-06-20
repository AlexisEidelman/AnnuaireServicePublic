# -*- coding: utf-8 -*-

import os

path_general_data = 'D:\data\Annuaire'

path = dict()

for extension in ['csv', 'zip', 'data', 'json']:
    folder_path = os.path.join(path_general_data, extension)
    path[extension] = folder_path
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
