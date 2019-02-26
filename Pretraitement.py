path = "data_scrapping/"
file = "tweets_2017-01-05_2017-04-10.csv"
import re
import os

def read_csv(path, file, nb_lines = 10):
    """Premier jet, utiliser l'autre"""
    f = open(path+file,'r')
    # tweet_id,user_id,user_pseudo,user_name,date_and_time,content,nb_replies,nb_retweets,nb_jaime
    Raw_data = f.readlines()
    
    Data = []
    nb_info = len(Raw_data[0][:-1].split(','))
    
    for i in range(1,min(len(Raw_data), nb_lines)):
        data = Raw_data[i][:-1].split(',') #trim \n, split
        tweet = ''
        for j in range(5, 5+ len(data)-nb_info): #gestion des virgules dans le tweet
            tweet = tweet + data[j]
        Data.append(data[:5]+[tweet]+data[6+ len(data)-nb_info:])

    f.close()
    return Data

def read_csv_unknown(path, file, nb_lines = 10000):
    """Fonction qui évite les caractères buggés"""
    f = open(path+file,'r', encoding="utf-8")
    # tweet_id,user_id,user_pseudo,user_name,date_and_time,content,nb_replies,nb_retweets,nb_jaime
    # Raw_data = f.readlines()
    
    Data = [] 
    nb_info = len(f.readline()[:-1].split(','))
    line = f.readline()
    i = 1
    while i < nb_lines+1 and line:
        try :
            data = line[:-1].split(',') #trim \n, split
            tweet = ''
            for j in range(5, 5+ len(data)-nb_info+1): #gestion des virgules dans le tweet
                tweet = tweet + data[j]
            Data.append(data[:5]+[tweet]+data[6+ len(data)-nb_info:])
            line = f.readline()
            i+=1
        except :
            print("aled")
    f.close()
    return Data

def affiche(Data):
    for d in Data:
        print(d)

def affiche_tweet(Data,nb = 10):
    for i in range(min(nb,len(Data))):
        print(Data[i][5])

def trim_tweet (tweet):
    """ Flag false -> No problem,
        Flag true  -> Destruction du tweet """
    no_tag = True
    t = tweet.split()
    L_clean = []
    for i in range(len(t)):
        if (t[i][:4]!="http" and t[i][:1]!="#"):
            if t[i][0] == "@":
                #                       WARNING,
                #   Comme j'ai pas la liste des gens, je peux pas encore identifier
                L_clean.append("thevoice" if t[i][:9]== "@thevoice" else "person")
                no_tag = False
            else :
                L_clean.append(t[i])
    
    tweet = ''
    for l in L_clean:
        tweet = tweet + l + " "
    #emoji = re.findall(r'[^\w\s,!:?;]', tweet)
    tweet = ''.join(re.findall(r'[0.123456789abcdefghijklmnopqrstuvwxyz ,!:?;]', tweet.lower()))
    return tweet, len(tweet) < 10 or len(re.findall(r'[éèàùã]', tweet))>0 or no_tag

def trim_data (Data,name_new_file = file[:-4]+"_clean.csv"):
    """Epure les tweets, donne le score d'importance et écrit dans le fichier"""
    # tweet_id,user_id,user_pseudo,user_name,date_and_time,content,nb_replies,nb_retweets,nb_jaime
    f = open("Cleaned/"+name_new_file,"w", encoding="utf-8")
    for i in range(len(Data)):
        clean_tweet, b = trim_tweet(Data[i][5])
        if not b :
            score_impor = int(Data[i][6])+int(Data[i][7])+int(Data[i][8])
            f.write(Data[i][0]+','+clean_tweet+','+str(score_impor)+'\n')
    f.close()

def clean_file (path, filename):
    """Nettoie tous les tweets d'un fichier"""
    Data = read_csv_unknown(path, filename)
    trim_data(Data, filename[:-4]+"_clean.csv")

def CLEAN_DIR (path):
    """Nettoie tous les tweets d'un dossier"""
    for filename in os.listdir(path):
        if filename.endswith(".csv"):
            Data = read_csv_unknown(path, filename)
            trim_data(Data, filename[:-4]+"_clean.csv")

