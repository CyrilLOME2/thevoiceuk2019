path = "data_scrapping/"
file = "tweets_2017-01-05_2017-04-10.csv"
import re
import os
from math import log

emoji = open('emoji.txt','w', encoding = "utf-8")


def importCoachs ():
    f = open("coachs.txt","r", encoding = 'utf-8')
    Lcoach = f.readlines()
    f.close()
    return [Lcoach[i][:-1] for i in range(len(Lcoach))]

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

def trim_tweet (tweet, Lcoach = []):
    """ Flag false -> No problem,
        Flag true  -> Destruction du tweet """
    no_tag, two_tags = True, False
    t = tweet.split()
    L_clean = []
    for i in range(len(t)):
        if not ("http" in t[i] or "#" in t[i]):
            if "@" in t[i] :
                if t[i] in Lcoach :
                    L_clean.append("coach")
                elif t[i][:9]== "@thevoice" :
                    L_clean.append("thevoice")
                else :
                    L_clean.append("candidate")
                    if not(no_tag) :
                        two_tags = True
                    no_tag = False
            else :
                L_clean.append(t[i])
    
    tweet = ''
    for l in L_clean:
        tweet = tweet + l + " "
    tweet_emojis = ''.join([tweet[i] for i in range(len(tweet)) if not (tweet[i] in ("0.123456789abcdefghijklmnopqrstuvwxyz ,!:?;']ABCDEFGHIJKLMNOPQRSTUVWXYZ()<>-_&%£’áóé~èç$€"+'"'))])
    emoji.write(tweet_emojis)
    tweet = ''.join(re.findall(r'[0.123456789abcdefghijklmnopqrstuvwxyz ,!:?;]', tweet.lower()))
    return tweet, (len(tweet) < 15 or len(re.findall(r'[éèàùã]', tweet))>0 or no_tag or two_tags)

def trim_data (Data,name_new_file = file[:-4]+"_clean.csv", Lcoach = []):
    """Epure les tweets, donne le score d'importance et écrit dans le fichier"""
    # tweet_id,user_id,user_pseudo,user_name,date_and_time,content,nb_replies,nb_retweets,nb_jaime
    f = open("Cleaned/"+name_new_file,"w", encoding="utf-8")
    f.write("idTweet, clean_tweet, scoreImportance, idCandidat\n")
    for i in range(len(Data)):
        clean_tweet, b = trim_tweet(Data[i][5], Lcoach)
        if not b :
            score_impor = int(log(2+int(Data[i][6])+int(Data[i][7])+int(Data[i][8]),10))
            f.write(Data[i][0]+','+clean_tweet+','+str(score_impor)+'\n')
    f.close()

def clean_file (path, filename):
    """Nettoie tous les tweets d'un fichier"""
    Data = read_csv_unknown(path, filename)
    Lcoach = importCoachs()
    trim_data(Data, filename[:-4]+"_clean.csv",Lcoach)

def CLEAN_DIR (path):
    """Nettoie tous les tweets d'un dossier"""
    for filename in os.listdir(path):
        if filename.endswith(".csv"):
            Data = read_csv_unknown(path, filename)
            trim_data(Data, filename[:-4]+"_clean.csv")
    try :
        emoji.close()
    except :
        pass
