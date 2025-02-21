# Recommandation de Séries Basée sur les Sous-Titres - SAE BUT3 S5

Ce projet propose un système de recommandation de séries TV basé sur les mots-clés trouvés dans les sous-titres des épisodes. L'objectif est de fournir des suggestions pertinentes en fonction des thèmes ou des sujets détectés dans le dialogue des séries.

## Fonctionnalités

- **Analyse des Sous-Titres** : Extraction de mots-clés et de thèmes à partir des fichiers de sous-titres des séries.
- **Recommandations Précises** : Suggestion de séries similaires en fonction des mots-clés identifiés.
- **Support Multilingue** : Détection et traitement des sous-titres dans plusieurs langues (anglais et français).
- **Interface Intuitive** : Interface simple et facile à utiliser pour rechercher et obtenir des recommandations de séries.

## Fonctionnenment

- **Nettoyage de fichiers SRT** : Un ensemble de scripts python nettoie tous les fichiers d'un .srt et txt contenant des sous-titres, les regroupent dans un seul fichier pour un traitement plus simple.
- **Traitement** : Ces dossiers contenant les fichiers de sous-titres sont parcourus et un calcul des matrices de TF-IDF est effectué puis ces matrices sont enregistrées dans des fichiers .npy (numpy) et .pkl (pickle)
- **Recommandation** : L'algorythme de recommandation prend en entré la matrices TF-IDF, le vectorizer du TF-IDF et une liste de mots saisie par l'utilisateur. Cette liste de mots et vectorizer et comparé au vecteur dans la matrices TF-IDF, qui renvoie une liste des 5 premiers match.
- **Affichage** : Grâce à son interface web simple, vous pouvez tapez vos mots clés dans une barre de recherche et obtenir vos résultats en temps réel en fonction des mots que vous tapé.

## Installation

- **Docker** : Tout d'abors il faut avoir docker-engine car ce projet se présente sous la forme d'une archive docker.
- ****
