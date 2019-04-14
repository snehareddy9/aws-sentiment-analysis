#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 00:01:26 2019

@author: sneha
"""

import re
from googlegeocoder import GoogleGeocoder
import configparser
import pandas as pd
import json
import nltk
from textblob import TextBlob


config = configparser.ConfigParser()
config.read('untitled1.init')

def clean_tweet(tweet): 
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def get_coordinates(s): 
    geocoder = GoogleGeocoder(config.get('api-tracker','google_api_key'))
    if s is None :
        return (None,None)
    else:     
        try:
            search = geocoder.get(s)
            if 'locality' in search[0].types:
                return (search[0].geometry.location.lat , search[0].geometry.location.lng)
            else: 
                return (None,None)
        except ValueError: 
            return (None, None)
        
def word_in_text(word, text):
    word = word.lower()
    text = text.lower()
    match = re.search(word, text)
    if match:
        return True
    return False  
        
def sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

def getfulltweet(tweet):
    try:
        return  tweet['extended_tweet']['full_text']
    except KeyError:
        try:
            return tweet['retweeted_status']['extended_tweet']['full_text']
        except KeyError:
            return tweet['text']
        

tweets_data = []
   
for line in open('/home/sneha/aws-project/sample.json', 'r'): 
    try:
        tweets_data.append(json.loads(line))
        #print(data)
    except: 
        continue

data = tweets_data[1:10]

tweets = pd.DataFrame()

tweets['created_at'] = list(map(lambda tweet: tweet['created_at'],data))
tweets['userid'] = list(map(lambda tweet: tweet['id'], data))
tweets['text'] = list(map(lambda tweet:getfulltweet(tweet), data))
tweets['cleaned_text'] = list(tweets['text'].apply(lambda tweet: clean_tweet(tweet)))
tweets['user_location'] = list(map(lambda tweet:tweet['user']['location'], data))
tweets['tweet_location'] = list(map(lambda tweet:tweet['place'], data))
#tweets['latitude'] = list(map(lambda tweet: get_coordinates(tweet['user']['location'])[0], data))
#tweets['longitude'] = list(map(lambda tweet:get_coordinates(tweet['user']['location'])[1], data))
tweets['donaldtrump'] = list(tweets['text'].apply(lambda tweet: word_in_text('#DonaldTrump', tweet)))
tweets['beto'] = list(tweets['text'].apply(lambda tweet: word_in_text('#Beto', tweet)))
tweets['berniesanders'] = list(tweets['text'].apply(lambda tweet: word_in_text('#BernieSanders', tweet)))
tweets['elizabethwarren'] = list(tweets['text'].apply(lambda tweet: word_in_text('#ElizabethWarren', tweet)))    
tweets['sentiment_polarity'] = list(tweets['cleaned_text'].apply(lambda tweet: sentiment(tweet)))
tweets['sentiment'] = list(tweets['sentiment_polarity'].apply(lambda tweet: 'Positive' if tweet > 0
      else ('Negative' if tweet < 0 else 'Neutral' ) ))
