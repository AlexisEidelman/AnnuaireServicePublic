# -*- coding: utf-8 -*-
"""

"""

import pandas as pd

tab = pd.read_csv('csv\\annuaire_20160905.csv', encoding='cp1252')
serie_exstension = tab['an/adresseCourriel'].str.split('@').str[1]

liste_extension = serie_exstension[serie_exstension.notnull()].unique()

gouvfr = [x for x in liste_extension if x[-7:] == 'gouv.fr']
ambassade = [x for x in liste_extension if 'ambafrance' in x]
not_gouvfr_nor_ambassade = [x for x in liste_extension
    if x not in gouvfr and x not in ambassade]

serie_exstension[serie_exstension.isin(not_gouvfr_nor_ambassade)].value_counts()
