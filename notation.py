# -*- coding: utf-8 -*-
"""
Created the 31/01/2019

@author: Cyril Lome for #thevoiceuk project

Component of the project that creates and applies the notation model
Based on Gensim library's Word2Vec

"""

# import modules & set up logging
import gensim, logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import numpy as np
import csv
import torch

# --------------------------------------------------------------------------------------------
#           PREPARAING THE DATA
# --------------------------------------------------------------------------------------------

def concatenateCSVs(filePath, fileNames):
    firstLine = True
    with open(filePath + 'total_tweets.csv', 'w', newline='', encoding="utf8") as fileToWrite:
        for fileName in fileNames:
            with open(filePath + fileName, encoding="utf8") as fileToRead:
                csvReader = csv.reader(fileToRead, delimiter=',')
                firstLine = True
                for row in csvReader:
                    if firstLine:
                        firstLine = False
                        print(row)
                        writer = csv.DictWriter(fileToWrite, fieldnames=row)
                        writer.writeheader()
                    else:
                        print(row)
                        tweet_info = {}
                        tweet_info['tweet_id'] = row[0]
                        tweet_info['user_pseudo'] = row[1]
                        tweet_info['user_id'] = row[2]
                        tweet_info['user_name'] = row[3]
                        tweet_info['date_and_time'] = row[4]
                        tweet_info['content'] = row[5]
                        tweet_info['nb_replies'] = row[6]
                        tweet_info['nb_retweets'] = row[7]
                        tweet_info['nb_jaime'] = row[8]
                        print(tweet_info)
                        writer.writerow(tweet_info)                        
                        

class SentencesIterator(object):
    """Iterator to go through the lines of a text file. The file must be constructed of one sentence by line.
    Using this iterator helps saving memory while processing the data.

    CONSTRUCTOR INPUT : directory path
    """

    def __init__(self, filePath):
        self.filePath = filePath
        self.categories = "tweet_id,user_id,user_pseudo,user_name,date_and_time,content,nb_replies,nb_retweets,nb_jaime".split(',')
        print('init finished')

    def __iter__(self):
        with open(self.filePath, encoding="utf8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            first_line = True
            for row in csv_reader:
                if first_line:
                    first_line = False
                    self.categories = row
                else:
                    # sentence = row[self.categories.index("content")].split()
                    # print(row[1])
                    sentence = row[1].split()
                    # print(sentence)
                    yield sentence
 
def read_input(input_file):
    """This method reads the input file which is in gzip format"""
 
    logging.info("reading file {0}...this may take a while".format(input_file))
    with gzip.open(input_file, 'rb') as f:
        for i, line in enumerate(f):
 
            if (i % 10000 == 0):
                logging.info("read {0} reviews".format(i))
            # do some pre-processing and return list of words for each review
            # text
            yield gensim.utils.simple_preprocess(line)
            
# --------------------------------------------------------------------------------------------
#           TRAINING & SAVING DIFFERENT MODELS
# --------------------------------------------------------------------------------------------
def create_model(sentences, modelName):
    bigram_transformer = gensim.models.Phrases(sentences)
    
    """model1 = gensim.models.Word2Vec(sentences)
    model1.save('model1')
    
    model2 = gensim.models.Word2Vec(sentences, min_count=10, size=200, workers=4)
    model2.save('model2')
    
    
    model3 = gensim.models.Word2Vec(bigram_transformer[sentences])
    model3.save('model3')
    
    model4 = gensim.models.Word2Vec(bigram_transformer[sentences], min_count=10, size=200, workers=4)
    model4.save('model4')
    
    model5 = gensim.models.Word2Vec(bigram_transformer[sentences], min_count=2, size=200, workers=4)
    model5.save('model5')
    
    model6 = gensim.models.Word2Vec(bigram_transformer[sentences], min_count=1, size=300, workers=4)
    model6.save('model6')"""
    
    # model7 = gensim.models.Word2Vec(bigram_transformer[sentences], min_count=1, size=300, workers=4)
    # model7.save('model7')
    
    model8 = gensim.models.Word2Vec(bigram_transformer[sentences], min_count=1, window=7, size=300, workers=4)
    model8.save(modelName)
    
    return model8

def load_model(modelName):
    model = gensim.models.Word2Vec.load(modelName)
    return model
# --------------------------------------------------------------------------------------------
#           TESTING THE MODEL
# --------------------------------------------------------------------------------------------

def test_model(model):
    print('Accuracy : ', model.wv.accuracy('test_questions.txt'))
    print('Similarity for "sing" : ', model.wv.most_similar(positive=['sing']))
    print('Similarity for "she" : ', model.wv.most_similar(positive=['she']))
    print('Similarity for "he" : ', model.wv.most_similar(positive=['he']))
    print('Similarity for "he" and "she" : ', model.wv.most_similar(positive=['he', 'she']))
    print('Similarity for "love" : ', model.wv.most_similar(positive=['love']))

# --------------------------------------------------------------------------------------------
#           TESTING THE MODEL
# --------------------------------------------------------------------------------------------

def avg_sentence_vector(words, model, num_features, index2word_set):
    """function to average all words vectors in a given paragraph
    Taken from : https://datascience.stackexchange.com/questions/23969/sentence-similarity-prediction
    """
    featureVec = np.zeros((num_features,), dtype="float32")
    nwords = 0

    for word in words:
        if word in index2word_set:
            nwords = nwords+1
            featureVec = np.add(featureVec, model.wv[word])
            # featureVec = np.add(featureVec, model.wv.__getitem__(word))

    if nwords>0:
        featureVec = np.divide(featureVec, nwords)
    return featureVec

def compare_avg_sentence_vectors(v1, v2):
    #return 1 - abs(sum(v1 - v2))
    return abs(sum(v1 - v2))

def test_sentence_model():
    vocab = model.wv.vocab
    # print(vocab.keys(), len(vocab))
    print(len(vocab))
    
    #get average vector for sentence 1
    sentence_1 = "I absolutely love The Voice"
    sentence_1_avg_vector = avg_sentence_vector(sentence_1.split(), model, model.trainables.layer1_size, vocab)
    
    #get average vector for sentence 2
    sentence_2 = "love"
    sentence_2_avg_vector = avg_sentence_vector(sentence_2.split(), model, model.trainables.layer1_size, vocab)
    
    #get average vector for sentence 2
    sentence_3 = "I hate The Voice"
    sentence_3_avg_vector = avg_sentence_vector(sentence_3.split(), model, model.trainables.layer1_size, vocab)
    
    # print(sentence_1_avg_vector - sentence_2_avg_vector)
    print(compare_avg_sentence_vectors(sentence_1_avg_vector, sentence_2_avg_vector))
    
    # print(sentence_1_avg_vector - sentence_1_avg_vector)
    print(compare_avg_sentence_vectors(sentence_1_avg_vector, sentence_3_avg_vector))
    
    # print(sentence_1_avg_vector - sentence_3_avg_vector)
    print(compare_avg_sentence_vectors(sentence_2_avg_vector, sentence_3_avg_vector))


# --------------------------------------------------------------------------------------------
#           APPLYING THE MODEL
# --------------------------------------------------------------------------------------------

# ------------ Méthode à faire EVOLUER pour avoir un modèle fonctionnel puis optimisé --------
def apply_model_to_sentence(sentence, sentenceToCompare, model):
    v1 = avg_sentence_vector(sentence.split(), model, model.trainables.layer1_size, model.wv.vocab)
    v2 = avg_sentence_vector(sentenceToCompare, model, model.trainables.layer1_size, model.wv.vocab)
    
    return compare_avg_sentence_vectors(v1, v2)

def apply_model_to_csv(filePath, fileName, modelTweetsFilePath, modelTweetsFileName, model):
    with open(filePath + 'results-' + fileName, 'w', newline='', encoding="utf8") as resultFile:
        with open(filePath + fileName, encoding="utf8") as fileToRead:
            csvReader = csv.reader(fileToRead, delimiter=',')
            firstLine = True
            writeHeaders = True
            for row in csvReader:
                if not firstLine:
                    tweet_info = {}
                    tweet_info['id_tweet'] = row[0]
                    tweet_info['id_candidate'] = row[3]
                    # tweet_info['content'] = row[1]
                    tweet_info['score_importance'] = row[2]
                    tweet_info['nb_smiley_happy'] = row[4]
                    tweet_info['nb_smiley_unhappy'] = row[5]
                    
                    tweet_content = row[1]
                    
                    count = 0
                    with open(modelTweetsFilePath + modelTweetsFileName, encoding="utf8") as modelTweetsFile:
                        modelTweetsCsvReader = csv.reader(modelTweetsFile, delimiter=',')
                        for row2 in modelTweetsCsvReader:
                            if count > 0:
                                tweet_info['w2v_' + str(count-1)] = apply_model_to_sentence(tweet_content, row2[1], model)
                            count +=1
                        
                    if writeHeaders:
                        #fieldNames = ["id_tweet", "content", "score_importance", "id_candidate", "nb_smiley_happy", "nb_smiley_unhappy"] + ['w2v_' + str(i-1) for i in range(1, count)]
                        fieldNames = ["id_tweet", "id_candidate", "score_importance", "nb_smiley_happy", "nb_smiley_unhappy"] + ['w2v_' + str(i-1) for i in range(1, count)]
                        writer = csv.DictWriter(resultFile, fieldnames=fieldNames)
                        writer.writeheader()
                        writeHeaders = False
                
                    writer.writerow(tweet_info)
                    
                firstLine = False

                    
def test_apply_model_to_csv(fileDirectory, fileName, modelTweetsFilePath, modelTweetsFileName, model):
    #apply_model_to_csv('data_scrapping/', 'total_tweets.csv', model)
    #apply_model_to_csv('Cleaned/', 'tweets_2017-01-05_2017-04-10_clean.csv', model)
    apply_model_to_csv(fileDirectory, fileName, modelTweetsFilePath, modelTweetsFileName, model)


# --------------------------------------------------------------------------------------------
#           KNN MODEL TO GET THE NOTATION
# --------------------------------------------------------------------------------------------

def apply_knn_to_csv(fileDirectory, fileName, modelTweetsFilePath, modelTweetsFileName, K):
    print(fileDirectory, fileName, modelTweetsFilePath, modelTweetsFileName)
    with open(fileDirectory + str(K) + 'nn-' + fileName, 'w', newline='', encoding="utf8") as resultFile:
        with open(fileDirectory + fileName, encoding="utf8") as fileToRead:
            csvReader = csv.reader(fileToRead, delimiter=',')
            firstLine = True
            writeHeaders = True
            for row in csvReader:
                if not firstLine:
                    tweet_info = {}
                    tweet_info['id_tweet'] = row[0]
                    tweet_info['id_candidate'] = row[1]
                    tweet_info['score_importance'] = row[2]
                    tweet_info['nb_smiley_happy'] = row[3]
                    tweet_info['nb_smiley_unhappy'] = row[4]
                    
                    tweetW2VTensor = torch.zeros(len(row) - 5)

                    for i in range(5, len(row)):
                        tweetW2VTensor[i-5] = float(row[i])
                        
                    sortedTweetW2VTensor, indices = torch.sort(tweetW2VTensor, descending=False)
                    knnIndices = indices[0:K]
                    
                    with open(modelTweetsFilePath + modelTweetsFileName, encoding="utf8") as resultFileToRead:
                        resultFileReader = csv.reader(resultFileToRead, delimiter=',')
                        notationsList = []

                        for row2 in resultFileReader:
                            try:
                                notationsList += [float(row2[2])]
                            except ValueError:
                                pass
                            
                        knnIndices = knnIndices.tolist()

                        for i in range(0, K):
                            index = knnIndices[i]
                            try:
                                tweet_info['notation_' + str(i+1)] = notationsList[index]
                            except IndexError as e:
                                print(index, len(notationsList))
    

                    if writeHeaders:
                        fieldNames = ["id_tweet", "id_candidate", "score_importance"] + ["notation_" + str(i+1) for i in range(0, K)] + ["nb_smiley_happy", "nb_smiley_unhappy"]
                        writer = csv.DictWriter(resultFile, fieldnames=fieldNames)
                        writer.writeheader()
                        writeHeaders = False
                
                    writer.writerow(tweet_info)
                    
                firstLine = False
                
                
if __name__ == "__main__":
    fileNames = ['tweets_2019-01-04_2019-01-30.csv', 'tweets_us_2014-02-22_2014-05-22.csv', 'tweets_us_2013-09-23_2013-12-17.csv', 'tweets_us_2013-03-23_2013-06-20.csv']
    filePath = "data_scrapping/"
    
    # concatenateCSVs(filePath, fileNames)
                    
    # sentences = SentencesIterator('data_scrapping/tweets_2019-01-04_2019-01-30.csv')
    #sentences = SentencesIterator('data_scrapping/total_tweets.csv')
    sentences = SentencesIterator('Cleaned/tweets_2017-01-05_2017-04-10_clean.csv')
    # sentences = read_input('data_scrapping/OpinRank-master.zip')
    
    model = create_model(sentences, "model_x")
    # apply_model_to_csv('Cleaned/', 'tweets_2017-01-05_2017-04-10_clean.csv', 'Cleaned/', 'test.csv', model)
    apply_model_to_csv('Cleaned/', 'tweets_2019-01-04_2019-01-30_clean.csv', 'Cleaned/', 'test.csv', model)

    #apply_knn_to_csv('Cleaned/', 'results-tweets_2017-01-05_2017-04-10_clean.csv', 'Cleaned/', 'test.csv', 1)
    #apply_knn_to_csv('Cleaned/', 'results-tweets_2017-01-05_2017-04-10_clean.csv', 'Cleaned/', 'test.csv', 3)
    apply_knn_to_csv('Cleaned/', 'results-tweets_2019-01-04_2019-01-30_clean.csv', 'Cleaned/', 'test.csv', 5)
