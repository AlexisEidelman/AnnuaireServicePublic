Ce dossier rassemble les informations sur les 
service public telles que contenu dans la base Sirene.

# Projet 

La base Sirene est une donnée de référence. Ce n'est pas pour autant qu'elle se suffit à elle-même. En effet, elle a des liens avec au moins deux autres données de référence : la **base adresses nationale** et l'**annuaire des services publics**.

Dans ce repo nous nous intéresserons essentiellement au lien entre la base SIRENE et l'annuaire des services publics.

Relier les entrées de la base Sirene avec les données de l'annuaire de l'administration publiées. Sont-elles cohérentes entre elles ? Lesquelles font référence ? Comment une modification de l'une des deux bases doit se propager à l'autre ? 


## Faisabilité 

Les données existent. En effet sur [cette page](http://www.insee.fr/fr/methodes/default.asp?page=definitions/sirene-secteur-public.htm) du site de l'Insee, on trouve le passage suivant :
Ou encore mieux [là](http://www.insee.fr/fr/methodes/default.asp?page=nomenclatures/agregatnaf2008/agregatnaf2008.htm)

>C'est en 1983 que la mission d'immatriculation au répertoire a été étendue au secteur public. L'unité SIREN est appelée organisme lorsqu'elle relève du secteur non marchand. Elle couvre donc normalement les personnes morales que constituent l'État, les collectivités territoriales et les établissements publics.
>
>Toutefois, certaines institutions et certains services de l'État, bien que non dotés de la personnalité juridique, sont identifiés comme organismes lorsqu'ils jouissent d'une « quasi-personnalité juridique ». C'est le cas des autorités constitutionnelles, des autorités administratives indépendantes, des ministères, des directions d'administration centrale ainsi que des services extérieurs, territorialisés ou non.
>
>L'unité SIRET de type établissement correspond soit à une implantation géographique distincte où s'exerce une activité, soit à une implantation géographique pour laquelle il existe un budget annexe. Ceci signifie que, contrairement au secteur privé, à une même adresse il peut exister plusieurs numéros SIRET pour un même numéro SIREN.



## Méthode

### Comment repérer les administrations publiques dans la base Sirene ?

Plusieurs idées :

* utiliser le code naf et en particulier [celles commençant par 84](http://www.insee.fr/fr/methodes/default.asp?page=nomenclatures/naf2008/n1_o.htm)
* utiliser [la nomenclature des catégories juridiques](http://www.insee.fr/fr/methodes/default.asp?page=nomenclatures/cj/cj-arbre.htm)

### Comment faire le lien entre SIRENE et Annuaire ?

La meilleure idée semble d'utiliser les noms des entités. On remarquera tout de suite que les formats sont différents (majuscules non accentuées dans un cas, simili Camel Case accentué dans l'autre).

Est-ce que les adresses peuvent aider ?

D'autres idées ? 

### Quel est le meilleure agencement des données de SIRENE et de l'annuaire ?

Des questions sont ouvertes :
* Comment gère-t-on les changements de noms ?
* Que faire des incohérences actuelles (s'il y en a).
* Quelle(s) adresse(s) doit-être conservée(s) ? Celle de l'annuaire ? Celle de SIRENE ?
* ...

