# Movie App avec Système de Recommandation
Une application web de découverte de films développée en Python avec Streamlit comme front-end. L'application utilise l'API The Movie Database (TMDB) pour obtenir des données en temps réel et propose un système de recommandation de films basé sur un dataset de 20 000 films.

Remarque : La fonctionnalité de recommandation n'est pas disponible en ligne à cause de la taille des fichiers .pkl, mais elle fonctionne parfaitement en local.

## Fonctionnalités
L'application est organisée en 4 pages Streamlit :

- Search.py : Recherchez un film en utilisant l'API TMDB.

- FilterByGenre.py : Filtrer les films par genre.

- Recommendation.py : Recommandation personnalisée basée sur la similarité entre les films (fonctionne uniquement en local).

- Watchlist.py : Créez et gérez votre propre watchlist.

## Système de Recommandation
Le moteur de recommandation utilise :

Un dataset de 20 000 films

Un calcul de similarité entre films stocké dans :

movies_list.pkl

similarity.pkl

Ces fichiers sont trop volumineux pour être hébergés sur GitHub, mais le système fonctionne localement.
