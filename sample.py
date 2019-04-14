#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 01:35:34 2019

@author: sneha
"""

import re
from googlegeocoder import GoogleGeocoder
import configparser

config = configparser.ConfigParser()
config.read('untitled1.init')

my_dict = {'created_at': 'Mon Apr 01 08:31:51 +0000 2019', 
'id': 1112633661558571008, 'id_str': '1112633661558571008', 
'text': 'This quote from our idoit @POTUS makes me want to give #ElizabethWarren money. https://t.co/Sk89i84hTD', 
'source': '<a href="http://twitter.com" rel="nofollow">Twitter Web Client</a>', 
'truncated': False, 'in_reply_to_status_id': None, 'in_reply_to_status_id_str': None, 
'in_reply_to_user_id': None, 'in_reply_to_user_id_str': None, 'in_reply_to_screen_name': None,
 'user': {'id': 3145828196, 'id_str': '3145828196', 'name': 'rev. andrew mazur', 
          'screen_name': 'revmazur', 'location': 'Madison, WI', 'url': None,
          'description': 'Bartender. Lefty. Atheist. Ordained Minister.', 'translator_type': 'none', 
          'protected': False, 'verified': False, 'followers_count': 38, 'friends_count': 432, 'listed_count': 0,
          'favourites_count': 764, 'statuses_count': 1134, 'created_at': 'Thu Apr 09 08:05:43 +0000 2015', 
          'utc_offset': None, 'time_zone': None, 'geo_enabled': False, 'lang': 'en', 'contributors_enabled': False, 
          'is_translator': False, 'profile_background_color': 'C0DEED', 
          'profile_background_image_url': 'http://abs.twimg.com/images/themes/theme1/bg.png', 
          'profile_background_image_url_https': 'https://abs.twimg.com/images/themes/theme1/bg.png', 
          'profile_background_tile': False, 'profile_link_color': '1DA1F2', 'profile_sidebar_border_color': 'C0DEED', 
          'profile_sidebar_fill_color': 'DDEEF6', 'profile_text_color': '333333', 'profile_use_background_image': True, 
          'profile_image_url': 'http://pbs.twimg.com/profile_images/1111417530965348358/nrNdy7Jo_normal.jpg', 
          'profile_image_url_https': 'https://pbs.twimg.com/profile_images/1111417530965348358/nrNdy7Jo_normal.jpg', 
          'default_profile': True, 'default_profile_image': False, 'following': None, 'follow_request_sent': None, 
          'notifications': None}, 'geo': None, 'coordinates': None, 'place': None, 'contributors': None, 
          'is_quote_status': False, 'quote_count': 0, 'reply_count': 0, 'retweet_count': 0, 'favorite_count': 0,
          'entities': {'hashtags': [{'text': 'ElizabethWarren', 'indices': [55, 71]}], 'urls': [{'url': 'https://t.co/Sk89i84hTD', 'expanded_url': 'https://www.nytimes.com/2019/03/31/us/politics/elizabeth-warren-fundraising.html', 'display_url': 'nytimes.com/2019/03/31/us/…', 'indices': [79, 102]}], 'user_mentions': [{'screen_name': 'POTUS', 'name': 'President Trump', 'id': 822215679726100480, 'id_str': '822215679726100480', 'indices': [26, 32]}], 'symbols': []}, 'favorited': False, 'retweeted': False, 'possibly_sensitive': False, 'filter_level': 'low', 'lang': 'en', 'timestamp_ms': '1554107511306'}


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
             

newdict = {}

newdict['created_at'] = my_dict['created_at']
newdict['userid'] = my_dict['id']
newdict['text'] = clean_tweet(my_dict['text'])
newdict['user_location'] = my_dict['user']['location']
newdict['tweet_location'] = my_dict['place']
newdict['latitude'] = get_coordinates(my_dict['user']['location'])[0]
newdict['longitude'] = get_coordinates(my_dict['user']['location'])[1]

print(newdict)




 
    
