# -*- coding: utf-8 -*-

import os

path_general_data = 'data/'

path = dict()

for extension in ['csv', 'zip', 'data', 'json']:
    folder_path = os.path.join(path_general_data, extension)
    path[extension] = folder_path
    if not os.path.isdir(folder_path):
        os.mkdir(folder_path)
