# osm-diff-to-text
Cet outil utilise les diff augmentés [1] afin d'aider les contributeurs à comprendre les modifications faites dans la base de données openstreetmap.

[1] http://wiki.openstreetmap.org/wiki/Overpass_API/Augmented_Diffs

# Utilisation
1. Téléchargez le programme
2. lancez la commande : python3 main.py %i , où %i est votre numéro de changeset

# Prérequis

Python 3+

# À faire

Le résultat est encore incomplet (et moche), il faudrait ajouter :
* la gestion des relations (si quelqu'un me passe un ou deux numéros de changeset je suis preneur)
* la gestion des déplacements d'objets ou d'ajout de points à un way
* internationaliser le résultat (via nominatim)
* ajouter la gestion de dates début/fin + une bbox (pour les cartoparties notamment)
* ... (liste trop longue)
