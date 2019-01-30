"""
Created the 24/01/2019

@author: Theo Ponton for #thevoiceuk project

The purpose of the script is to extract tweets with the hastag #thevoiceuk between two dates.
The result will be store into a csv file named tweets_<dtae1>_<date2>.csv

"""

# importing libraries
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from datetime import datetime, timedelta, date

def date_str_to_date(date_str):
    date_list = date_str.split('-')
    return date(int(date_list[0]), int(date_list[1]), int(date_list[2]))

def date_date_to_str(date_date):
    date_day = str(date_date.day)
    if len(date_day) == 1:
        date_day = '0' + date_day
    date_month = str(date_date.month)
    if len(date_month) == 1:
        date_month = '0' + date_month
    date_year = str(date_date.year)
    return date_year + '-' + date_month + '-' + date_day

def get_next_day(date_str):
    date_date = date_str_to_date(date_str)
    date_date = date_date + timedelta(days=1)
    date_str = date_date_to_str(date_date)
    return date_str

# asking for the dates
date_debut = str(input('Please choose date_debut. Ex : 2019-01-04\n>>>'))
date_fin = str(input('Please choose date_fin. Ex : 2019-01-30\n>>>'))
# date_debut = '2019-01-04'
# date_fin = '2019-01-30'

date_1 = date_debut
date_2 = get_next_day(date_1)
print(date_1, date_2)

# where to store de data
tweets_info = []

# creating selenium driver
binary = FirefoxBinary(r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe')
executable_path = r'C:\Users\theop\Documents\Cours\Projet Option\thevoiceuk2019\data_scrapping\geckodriver.exe'
driver = webdriver.Firefox(firefox_binary=binary, executable_path=executable_path)

while date_1 != date_fin :

    # reaching the result page
    print('Reaching the page...')
    link = 'https://twitter.com/search?l=&q=%23thevoiceuk%20since%3A' + date_1 + '%20until%3A' + date_2 + '&src=typd'
    driver.get(link)
    time.sleep(5)

    # scroll down till the end
    print('Scrolling down...')
    iter = 0
    id_last_tweet = driver.find_elements_by_xpath("//li[@data-item-type='tweet']/div")[-1].get_attribute('data-tweet-id')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    id_last_tweet_2 = driver.find_elements_by_xpath("//li[@data-item-type='tweet']/div")[-1].get_attribute('data-tweet-id')
    while id_last_tweet != id_last_tweet_2 and iter < 50:
        iter += 1
        id_last_tweet = id_last_tweet_2
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        id_last_tweet_2 = driver.find_elements_by_xpath("//li[@data-item-type='tweet']/div")[-1].get_attribute(
            'data-tweet-id')

    print('We scrolled down ' + str(iter) + ' times !')

    # localize each tweet
    print('Finding information...')
    tweets = driver.find_elements_by_xpath("//li[@data-item-type='tweet']/div")
    print('Number of tweets : ' + str(len(tweets)))
    for tweet in tweets:
        tweet_info = {}
        tweet_info['tweet_id'] = tweet.get_attribute('data-tweet-id')
        tweet_info['user_pseudo'] = tweet.get_attribute('data-screen-name')
        tweet_info['user_id'] = tweet.get_attribute('data-user-id')
        tweet_info['user_name'] = tweet.get_attribute('data-name')
        tweet_info['date_and_time'] = str(tweet.find_element_by_xpath("//div[@data-tweet-id='" + tweet_info['tweet_id'] + "']/div/div/small/a[@class='tweet-timestamp js-permalink js-nav js-tooltip']").get_attribute('title'))
        tweet_info['content'] = tweet.find_element_by_xpath("//div[@data-tweet-id='" + tweet_info['tweet_id'] + "']/div/div[@class='js-tweet-text-container']").text.replace('\n', ' ')
        tweet_info['nb_replies'] = tweet.find_element_by_xpath("//span[@id='profile-tweet-action-reply-count-aria-" + tweet_info['tweet_id'] + "']").get_attribute('innerHTML')[0]
        tweet_info['nb_retweets'] = tweet.find_element_by_xpath(
            "//span[@id='profile-tweet-action-retweet-count-aria-" + tweet_info['tweet_id'] + "']").get_attribute(
            'innerHTML')[0]
        tweet_info['nb_jaime'] = tweet.find_element_by_xpath(
            "//span[@id='profile-tweet-action-favorite-count-aria-" + tweet_info['tweet_id'] + "']").get_attribute(
            'innerHTML')[0]
        tweets_info.append(tweet_info)

    date_1 = date_2
    date_2 = get_next_day(date_1)

    print('\n')
    print(date_1, date_2)

# csv output
print('Writing csv file...')
with open('tweets_' + date_debut + '_' + date_fin + '.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['tweet_id', 'user_id', 'user_pseudo', 'user_name', 'date_and_time', 'content', 'nb_replies', 'nb_retweets', 'nb_jaime']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for tweet_info in tweets_info:
        writer.writerow(tweet_info)