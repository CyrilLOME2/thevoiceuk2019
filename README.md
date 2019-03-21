# The Voice UK 2019
Nous sommes 3 élèves de l'Ecole Centrale de Lyon en option informatique : Cyril Lome, Denis Guibert et Théo Ponton. Le but de notre projet est de determiner le gagnant de The Voice UK 2019 à travers une analyse de tweets. 

## Résumé

Dans l'idée, nous allons dans un premier temps récupérer des tweets ayant de hashtag #TheVoiceUK. Ces tweets bruts vont être traités afin de filtrer les tweets n'apportant aucune information, d'éliminer certains caractères spéciaux, ... Il faudra ensuite determiner pour chaque tweet la personne dont il est question. Ensuite, ces tweets vont passer dans un modèle Word2Vec. Il sera entrainé grâce à des tweets des années précédentes. Il permettra de calculer des distances entre des tweets dont on aura donné une note entre 1 et 5 "à la main" et les tweets de la saison actuelle. Via un algorithme des K-Plus-Proches-Voisins, nous allons pouvoir avoir une note pour notre tweet. Chaque tweet aura ensuite plus ou moins d'importance en fonction du nombre de retweets, commentaires  et mentions j'aime. Pour chaque personne, nous allons donc additionner la note de chacun de leur tweet multiplié par l'importance du tweet. Cela va créer un score. Le candidat ayant le score le plus élévé sera le vainqueur que nous allons prédire. 

