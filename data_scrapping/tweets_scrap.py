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

# asking for the dates
# date_1 = str(input('Please choose date_1. Ex : 2019-01-01\n>>>'))
# date_2 = str(input('Please choose date_2. Ex : 2019-01-03\n>>>'))
date_1 = '2019-01-04'
date_2 = '2019-01-07'

# creating selenium driver
binary = FirefoxBinary(r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe')
executable_path = r'C:\Users\theop\Documents\Cours\Projet Option\thevoiceuk2019\data_scrapping\geckodriver.exe'
driver = webdriver.Firefox(firefox_binary=binary, executable_path=executable_path)

# reaching the result page
link = 'https://twitter.com/search?l=&q=%23thevoiceuk%20since%3A' + date_1 + '%20until%3A' + date_2 + '&src=typd'
driver.get(link)
time.sleep(5)

# where to store de data
tweets_info = []

# localize each tweet
tweets = driver.find_elements_by_xpath("//li[@data-item-type='tweet']/div")
for tweet in tweets:
    tweet_info = {}
    tweet_info['tweet_id'] = tweet.get_attribute('data-tweet-id')
    tweet_info['user_pseudo'] = tweet.get_attribute('data-screen-name')
    tweet_info['user_id'] = tweet.get_attribute('data-user-id')
    tweet_info['user_name'] = tweet.get_attribute('data-name')
    tweet_info['date_and_time'] = str(tweet.find_element_by_xpath("//div[@data-tweet-id='" + tweet_info['tweet_id'] + "']/div/div/small/a[@class='tweet-timestamp js-permalink js-nav js-tooltip']").get_attribute('title'))
    tweet_info['content'] = tweet.find_element_by_xpath("//div[@data-tweet-id='" + tweet_info['tweet_id'] + "']/div/div[@class='js-tweet-text-container']").text.replace('\n', ' ')
    tweets_info.append(tweet_info)
    print(tweet_info)

# csv output
with open('tweets_' + date_1 + '_' + date_2 + '.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['tweet_id', 'user_id', 'user_pseudo', 'user_name', 'date_and_time', 'content']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for tweet_info in tweets_info:
        writer.writerow(tweet_info)