Ce dossier rassemble les informations sur les 
service public telles que contenu dans la base Sirene.

Projet 
====

Relier les entrées de la base Sirene avec les données de l'annuaire de 
l'administration publiées. Sont-elles cohérentes ? Lesquelles font 
référence ?


Faisabilité 
====

Les données existent. En effet sur [cette page](http://www.insee.fr/fr/methodes/default.asp?page=definitions/sirene-secteur-public.htm) du site de l'Insee, on trouve le passage suivant :
Ou encore mieux [là](http://www.insee.fr/fr/methodes/default.asp?page=nomenclatures/agregatnaf2008/agregatnaf2008.htm)

    C'est en 1983 que la mission d'immatriculation au répertoire a été étendue au secteur public. L'unité SIREN est appelée organisme lorsqu'elle relève du secteur non marchand. Elle couvre donc normalement les personnes morales que constituent l'État, les collectivités territoriales et les établissements publics.

    Toutefois, certaines institutions et certains services de l'État, bien que non dotés de la personnalité juridique, sont identifiés comme organismes lorsqu'ils jouissent d'une « quasi-personnalité juridique ». C'est le cas des autorités constitutionnelles, des autorités administratives indépendantes, des ministères, des directions d'administration centrale ainsi que des services extérieurs, territorialisés ou non.
    L'unité SIRET de type établissement correspond soit à une implantation géographique distincte où s'exerce une activité, soit à une implantation géographique pour laquelle il existe un budget annexe. Ceci signifie que, contrairement au secteur privé, à une même adresse il peut exister plusieurs numéros SIRET pour un même numéro SIREN.



Méthode
====

Comment repérer les administrations publiques ? 
Plusieurs idées :

* utiliser le code naf et en particulier [celles commençant par 84](http://www.insee.fr/fr/methodes/default.asp?page=nomenclatures/naf2008/n1_o.htm)
* utiliser [la nomenclature des catégories juridiques](http://www.insee.fr/fr/methodes/default.asp?page=nomenclatures/cj/cj-arbre.htm)
