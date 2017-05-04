# -*- coding: utf-8 -*-
"""

"""

import pandas as pd

from annuaire.load import load_csv

tab = load_csv('20170315.csv')

exstension_mail = tab['an/adresseCourriel'].str.split('@').str[1]
exstension_mail = exstension_mail[exstension_mail.notnull()]
liste_extension = exstension_mail.unique()


gouvfr = [x for x in liste_extension if x[-7:] == 'gouv.fr']
ambassade = [x for x in liste_extension if 'ambafrance' in x]
parcnational = [x for x in liste_extension if 'parcnational' in x] 
# parcnation inclut parcnational.fr sans prefixe

autres_extension = [x for x in liste_extension
    if x not in gouvfr and x not in ambassade and x not in parcnational]

exstension_mail[exstension_mail.isin(autres_extension)].value_counts()

