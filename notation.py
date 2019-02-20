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
                        
fileNames = ['tweets_2019-01-04_2019-01-30.csv', 'tweets_us_2014-02-22_2014-05-22.csv', 'tweets_us_2013-09-23_2013-12-17.csv', 'tweets_us_2013-03-23_2013-06-20.csv']
filePath = "data_scrapping/"

# concatenateCSVs(filePath, fileNames)

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
        with open('data_scrapping/tweets_2019-01-04_2019-01-30.csv', encoding="utf8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            first_line = True
            for row in csv_reader:
                if first_line:
                    first_line = False
                    self.categories = row
                else:
                    sentence = row[self.categories.index("content")].split()
                    # print(sentence)
                    yield sentence
    

# sentences = SentencesIterator('data_scrapping/tweets_2019-01-04_2019-01-30.csv')
sentences = SentencesIterator('data_scrapping/total_tweets.csv')

# --------------------------------------------------------------------------------------------
#           TRAINING THE MODEL
# --------------------------------------------------------------------------------------------

model = gensim.models.Word2Vec(sentences, min_count=10, size=200, workers=4)


# --------------------------------------------------------------------------------------------
#           TESTING THE MODEL
# --------------------------------------------------------------------------------------------

print('Accuracy : ', model.wv.accuracy('test_questions.txt'))
print('Similarity for "sing" : ', model.wv.most_similar(positive=['sing']))
print('Similarity for "she" : ', model.wv.most_similar(positive=['she']))
print('Similarity for "he" : ', model.wv.most_similar(positive=['love']))
print('Similarity for "he" and "she" : ', model.wv.most_similar(positive=['he', 'she']))

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
    return 1 - abs(sum(v1 - v2))

vocab = model.wv.vocab

#get average vector for sentence 1
sentence_1 = "I absolutely love The Voice"
sentence_1_avg_vector = avg_sentence_vector(sentence_1.split(), model, 200, vocab)

#get average vector for sentence 2
sentence_2 = "love"
sentence_2_avg_vector = avg_sentence_vector(sentence_2.split(), model, 200, vocab)

#get average vector for sentence 2
sentence_3 = "I love The Voice"
sentence_3_avg_vector = avg_sentence_vector(sentence_3.split(), model, 200, vocab)

# print(sentence_1_avg_vector - sentence_2_avg_vector)
print(compare_avg_sentence_vectors(sentence_1_avg_vector, sentence_2_avg_vector))

# print(sentence_1_avg_vector - sentence_1_avg_vector)
print(compare_avg_sentence_vectors(sentence_1_avg_vector, sentence_3_avg_vector))

# print(sentence_1_avg_vector - sentence_3_avg_vector)
print(compare_avg_sentence_vectors(sentence_2_avg_vector, sentence_3_avg_vector))
