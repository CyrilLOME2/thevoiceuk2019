# The Voice UK 2019
Nous sommes 3 élèves de l'Ecole Centrale de Lyon en Option Informatique : Cyril Lome, Denis Guibert et Théo Ponton. Le but de notre projet est de determiner le gagnant de The Voice UK 2019 à travers une analyse de tweets. Ce projet s'inscrit dans la formation de Semestre 9 et a été encadré par l'enseignant-chercheur de l'ECL Alexandre SAIDI.

## Résumé

Dans l'idée, nous avons dans un premier temps récupéré des tweets ayant de hashtag #TheVoiceUK. Ces tweets bruts ont été traités afin de filtrer les tweets n'apportant aucune information, d'éliminer certains caractères spéciaux, ... Il a fallu ensuite determiner pour chaque tweet la personne dont il était question. Ensuite, ces tweets sont passés dans un modèle Word2Vec. Il a été entrainé grâce à des tweets des années précédentes. Il a permi de calculer des distances entre des tweets dont on avait au préalable donné une note entre 1 et 5 "à la main" et les tweets de la saison actuelle. Via un algorithme des K-Plus-Proches-Voisins, nous avons pu avoir une note pour chaque tweet (toujours entre 1 et 5). Chaque tweet a plus ou moins d'importance en fonction du nombre de retweets, commentaires  et mentions j'aime. Pour chaque candidat, nous avons donc additionné la note de chacun de leur tweet multiplié par l'importance du tweet. Cela a créer un score pour chacun d'entre eux. Le candidat ayant le score le plus élévé est notre vainqueur. 

## Requirements

Afin de faire exécuter notre projet sur votre machine, il faut :
- Installer le module python `Gensim` (https://pypi.org/project/gensim/)
- Installer le module python `Selenium` (https://www.seleniumhq.org/download/)
- Installer le module python `Pytorch` (https://pytorch.org/)
- Télécharger le `GeckoDriver` (https://github.com/mozilla/geckodriver/releases) et le placer dans la directory `data_scrpping\tweets_scrap.py`

## Structure générale du projet

Le projet est consistué de cinq scripts python :
- `data_scrapping\tweets_scrap.py` effectue le data-scrapping
- `Pretraitement.py` traite les données issues du data-scrapping pour les rendre utilisables
- `notation.py` traite les données en calculant une note pour chaque tweet
- `algo_final.py` fait la synthèse des tweets notés pour trouver le classement des candidats
- `main.py` fait tourner l'ensemble de l'algorithme en appelant les méthodes définies dans les scripts ci-dessus

Le projet est également divisé en plusieurs directories :
- la directory de base contient la plupart des scripts python, les fichiers statiques ainsi que le modèle Word2Vec construit
- la directory `data_scrapping` contient tous les résultats des étapes de data-scrapping
- la directory `Cleaned` contient l'ensemble des fichiers de tweets pré-traités
- la directory `Labelled` contient les tweets labellisés servant aux modèles W2V et KNN
- la directory `Results` contient les résultats finaux de l'exécution de notre projet

## Algorithme de data-scrapping

L'algorithme de Data Scraping est le point de départ du projet. Son but est de récolter tous les tweets avec le hashtag #TheVoiceUK entre deux dates *date1* et *date2*. Pour le lancer, il suffit d'aller dans le dossier */data_scrapping* et de lancer *tweets_scrap.py*. L'algorithme va alors demander les deux dates sous un certain format. Une fois les deux dates données, le driver Geckodriver va naviguer sur Firefox et parcourir le code HTML afin d'avoir les informations nécessaires. En sortie, l'algorithme va inscrire l'ensemble de ces informations dans un fichier csv dans  */data_scrapping* intitulé *tweets_date1_date2.csv*. 

Ce fichier va contenir les informations suivantes : id du tweet, id du user, pseudo, nom du user, date et heure, contenu du tweet, nombre de commentaires, nombre de retweets, nombre de mentions j'aime. 

Il peut être utilisé pour tout type de recherche de tweets sur twitter entre 2 dates. Il suffit d'aller sur <https://twitter.com/search-advanced?lang=en>, de faire sa recherche entre les deux dates. Vous allez être redirigés vers twitter. Copiez l'URL et remplacez cette ligne de code :

```python
link = 'https://twitter.com/search?l=&q=%23thevoiceuk%20since%3A' + date_1 + '%20until%3A' + date_2 + '&src=typd'
```

par votre URL, en veillant à bien mettre date_1 et date_2 au bon endroit.

## Algorithme de prétraitement

L'algorithme de *Prétraiment.py* est en charge du tri préliminaire des tweets ainsi que de la correction et l'adaptation du contenu du tweeet au processing Word2Vec. On retrouve dans ce fichier des fonctions d'import de la liste des coachs, mais aussi *read_csv_unknown*, qui est une fonction d'import de tweet qui supprime déjà les caractères trop étranges qui faisaient planter l'algorithme. Ensuite, on envoie ces données importées dans *trim_data* qui gère la mise en place du score d'importance ainsi que l'écriture sur le fichier cleaned. Cependant, avant d'écrire la version "cleaned", il faut passer le tweet dans la fonction *trim_tweet*.

La fonction *trim_tweet* s'occupe de :
  - supprimer les mots sans sens (les #hashtags, les liens internets, ...)
  - analyser les identifications, avec les coachs, les candidats 2019 si les données sont de 2019...
  - rejeter les mauvais tweets (tweets sans candidat, trop courts, ayant des accents/caractères étrangers...)
  - trouver les smileys, ou emojis, et donner le score correspondant
  - rendre le tweet facile à macher pour Word2Vec par la suite
 
 Enfin, on peut utiliser les fonctions valises *clean_file* et *CLEAN_DIR* qui permettent de "clean" respectivement un fichier csv, ou l'intégralité des csv d'un dossier.

## Utilisation du framework Word2Vec

Le framework Word2Vec est importé à travers le module python `Gensim`. Il permet de créer des modèles qui font correspondre à des mots des vecteurs, de par leurs voisins fréquents dans un texte. Ainsi, la représentation d'un mot par W2V est calculée en fonction des mots qui l'entourent le plus souvent. Deux mots similaires arrivant généralement entre les mêmes mots, ils auront donc une représentation vectorielle similaire.

De là, on peut représenter une phrase comme la moyenne des vecteurs de ses mots. Deux phrases pourront être comparées en prenant la valeur absolue de la différence entre leurs vecteurs.

Dans notre projet, nous entraînons un modèle Word2Vec avec 3723 tweets (phrases) issus des éditions 2014 à aujourd'hui de The Voice UK et The Voice US. Un mot est représenté par un vecteur de taille 300 et Word2Vec parcourt chaque phrase avec une fenêtre de 7 mots pour étudier un mot.

Pour prendre en main Word2Vec de Gensim sous python, nous avons utilisé le tutoriel de Radim Řehůřek (https://rare-technologies.com/word2vec-tutorial/)

## Algorithme de notation

### 0. Labellisation de tweets
Pour la suite, on aura besoin de tweets possédant déjà un note d'avis, afin d'utiliser un algorithme à apprentissage supervisé. Ainsi, dans la directory `Labelled`, nous avons construit un fichier au format CSV contenant des tweets et les notes (que nous avons entrées à la main selon notre propre jugement) correspondantes. Nous avons 200 tweets labellisés. L'algorithme de notation s'effectue alors en deux temps :

### 1. Application du modèle Word2Vec
On compare le tweet aux 200 tweets labellisés, selon le modèle Word2Vec. On construit ainsi un fichier CSV de la même forme, mais chaque tweet possède en plus 200 nouvelles colones : chacune contient la similarité W2V avec l'un des tweets labellisés.

### 2. Application d'un algorithme de KNN
A partir du CSV construit juste ci-dessus, on peut maintenant trouver les K tweets labellisés les plus proches de chaque tweets. En prenant la moyenne des notes de ces K tweets labellisés les plus proches, on peut donner une note à chacun des tweets. On enregistre les résultats dans un fichier CSV.

## Algorithme final
L'algorithme final prend l'ensemble des tweets notés issus de l'algorithme de notation et applique la formule suivante, pour chaque candidat :

Score(candidat) = somme_{t in tweets(candidate)} [ (5 * note(t) + smileys(t)) * log(puissance(t)) / 6 ]

où puissance(t) = commentaires(t) + likes(t) + retweets(t)

