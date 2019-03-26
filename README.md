# The Voice UK 2019
Nous sommes 3 élèves de l'Ecole Centrale de Lyon en option informatique : Cyril Lome, Denis Guibert et Théo Ponton. Le but de notre projet est de determiner le gagnant de The Voice UK 2019 à travers une analyse de tweets. 

## Résumé

Dans l'idée, nous avons dans un premier temps récupéré des tweets ayant de hashtag #TheVoiceUK. Ces tweets bruts ont été traités afin de filtrer les tweets n'apportant aucune information, d'éliminer certains caractères spéciaux, ... Il a fallu ensuite determiner pour chaque tweet la personne dont il était question. Ensuite, ces tweets sont passés dans un modèle Word2Vec. Il a été entrainé grâce à des tweets des années précédentes. Il a permi de calculer des distances entre des tweets dont on avait au préalable donné une note entre 1 et 5 "à la main" et les tweets de la saison actuelle. Via un algorithme des K-Plus-Proches-Voisins, nous avons pu avoir une note pour chaque tweet (toujours entre 1 et 5). Chaque tweet a plus ou moins d'importance en fonction du nombre de retweets, commentaires  et mentions j'aime. Pour chaque candidat, nous avons donc additionné la note de chacun de leur tweet multiplié par l'importance du tweet. Cela a créer un score pour chacun d'entre eux. Le candidat ayant le score le plus élévé est notre vainqueur. 

## Requirements

Afin de faire exécuter notre projet sur votre machine, il faut :
- Installer le module python Gensim (https://pypi.org/project/gensim/)
- Installer le module python Selenium (https://www.seleniumhq.org/download/)

## Structure générale du projet

## Algorithme de data-scrapping

## Algorithme de prétraitement

## Utilisation du framework Word2Vec

## Algorithme de notation

## Algorithme final

