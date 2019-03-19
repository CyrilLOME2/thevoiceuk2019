"""
Created the 14/03/2019

@author: All team members from for #thevoiceuk project

This script will import all the functions that have been done during to project to build the whiole data pipeline
from data srapping to the final ranking.

"""
from data_scrapping.tweets_scrap import *
from algo_final import *
from notation import *
from Pretraitement import *

print('coucou')


# -----------------------------------------------------------------------------
#           WORD2VEC (W2V) MODEL Creation
# -----------------------------------------------------------------------------

createW2VModel = True # set to False if you have already created the W2V model

if createW2VModel:
    # Let w2vTweetsFilePath be the relative path to the csv file containing all the tweets that W2V has to take for training
    w2vTweetsFilePath = 'à ajouter !!'
    sentences = SentencesIterator(w2vTweetsFilePath)
    model = create_model(sentences, "final_model")
    # Then you will have your W2V model created in the current directory as "final_model"
else:
    model = load_model("final_model")


# -----------------------------------------------------------------------------
#           Apply the W2V MODEL comparison to the tweets to evaluate
# -----------------------------------------------------------------------------
    
# Let :
#   - tweetsToEvaluateFilePath be the path to the directory containing the file of the tweets to evaluate
#   - tweetsToEvaluateFileName be the name of the file containing the tweets to evaluate
#   - modelTweetsFilePath be the path to the directory containing the file of the labelled tweets for W2V comparison
#   - modelTweetsFileName be the name of the file containing the labelled tweets for W2V comparison
#   - model be the W2V model
    
tweetsToEvaluateFilePath = "\Cleaned"
tweetsToEvaluateFileName = "cleaned_tweets.csv"

modelTweetsFilePath = "\Labelled"
modelTweetsFileName = "labelled_tweets.csv"

apply_model_to_csv(tweetsToEvaluateFilePath, tweetsToEvaluateFileName, modelTweetsFilePath, modelTweetsFileName, model)

# Then you will have a csv created at the same directory as the tweets to evaluate. This csv has the same name with "results-" prepended.

# -----------------------------------------------------------------------------
#           Apply the KNN model to get the notation of each tweets
# -----------------------------------------------------------------------------

# Let :
#   - tweetsToEvaluateFilePath be the path to the directory containing the file of the tweets to evaluate (they must have past the W2V evaluation)
#   - tweetsToEvaluateFileName be the name of the file containing the tweets to evaluate (they must have past the W2V evaluation)
#   - modelTweetsFilePath be the path to the directory containing the file of the labelled tweets for W2V comparison
#   - modelTweetsFileName be the name of the file containing the labelled tweets for W2V comparison
#   - K be the K attribute of the KNN algorithm

tweetsToEvaluateFilePath = "\Cleaned"
tweetsToEvaluateFileName = "results-cleaned_tweets.csv"

modelTweetsFilePath = "\Labelled"
modelTweetsFileName = "labelled_tweets.csv"

apply_knn_to_csv(tweetsToEvaluateFilePath, tweetsToEvaluateFileName, modelTweetsFilePath, modelTweetsFileName, K)

# Then you will have a csv created at the same directory as the tweets to evaluate. This csv has the same name with "knn-" prepended.

