#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 00:06:08 2019

@author: sneha
"""

#import boto3
#import random
import math
import time
import json
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import configparser

tweepy.debug(True)
config = configparser.ConfigParser()
config.read('untitled1.init')

auth = OAuthHandler(config.get('api-tracker','consumer_key'),config.get('api-tracker','consumer_secret'))
auth.set_access_token(config.get('api-tracker', 'access_token'), config.get('api-tracker','access_token_secret'))

# Open/Create a file to append data
#csvFile = open('/home/sneha/aws-project/tweetdata/tweets.csv', 'a')
#Use csv Writer
#fields = ('created_at','user_id','text', 'coordinates','place', 'followers')
#csvWriter = csv.writer(csvFile, lineterminator= '\n')


class StdOutListener(StreamListener):
    def __init__(self,path=None):
        self.path = path
        self.siesta = 0
        self.nightnight = 0
        self.count = 0
        
    def on_data(self, data):
        #client.put_record(DeliveryStreamName=DeliveryStreamName,Record={'Data': json.loads(data)["text"]})
        x = json.loads(data)
        self.count = self.count+1
        print("count is :"+str(self.count))
        with open('sample.json', 'a') as f: 
            f.write('\n')
            json.dump(x,f)
        return True
    
    def on_error(self, status_code):
        print('Error:', str(status_code))
        if status_code == 420:
            sleepy = 60 * math.pow(2, self.siesta)
            print(time.strftime("%Y%m%d_%H%M%S"))
            print("A reconnection attempt will occur in " + str(sleepy/60) + " minutes.")
            time.sleep(sleepy)
            self.siesta += 1
        else:
            sleepy = 5 * math.pow(2, self.nightnight)
            print(time.strftime("%Y%m%d_%H%M%S"))
            print("A reconnection attempt will occur in " + str(sleepy) + " seconds.")
            time.sleep(sleepy)
            self.nightnight += 1
        return True 
        
while True:
    try:
        stream = Stream(auth, StdOutListener())
        stream.filter(languages = ['en'],  track=['#BernieSanders','#Beto','#ElizabethWarren','#DonaldTrump'])
    except:
        print("Exception occured")
        continue
              
              
              #locations = [-125.0011, 24.9493, -66.9326, 49.5904],




