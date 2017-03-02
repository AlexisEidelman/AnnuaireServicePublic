# AnnuaireServicePublic
Utilisation de l'annuaire du service public 

## Trouver les données
Les données peuvent être téléchargées sur le site [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/service-public-fr-annuaire-de-ladministration-base-de-donnees-nationales/)

## De rdf à csv
Les données sont diffusées dans un format rdf. Le code permet de générer une base csv. Cette base est postée comme ressource communautaire supplémentaire sur la page correspondante de [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/service-public-fr-annuaire-de-ladministration-base-de-donnees-nationales/)

## De rdf à json
Comme pour le csv, le format json peut aussi être généré via ce fichier.

## Une visualisation
On peut afficher une représentation des données via ce lien : [http://alexiseidelman.github.io/AnnuaireServicePublic/](http://alexiseidelman.github.io/AnnuaireServicePublic/). 
Toute contribution est la bienvenue !

## Des idées
À terme, j'aimerais produire un organigramme complet de l'administration publique (au moins à partir de la base de données nationale). 

Je voudrais aussi permettre de visualiser les évolutions : quelles organisations changent et quand ? 
Pour cela, il faudrait un historique des données.

* Ajouter les données de la base SIRENE pour enrichir la base.

On trouve ici un [exemple](http://data.enseignementsup-recherche.gouv.fr/pages/explorer/?sort=modified&refine.publisher=Minist%C3%A8re%20de%20l%27%C3%89ducation%20nationale,%20de%20l%27Enseignement%20sup%C3%A9rieur%20et%20de%20la%20Recherche&q=siret) d'administrations avec un siret (à étudier).

Voir comment les données sont dans le fichier SIRENE. Est-ce que l'on peut faire un lien avec les données.
