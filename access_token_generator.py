#!/usr/bin/env python
# encoding: utf-8
"""
access_token_generator.py

Written by Martin Gammelsæter (@martingamm)

"""
from oauthtwitter import OAuthApi
import ConfigParser

# Opens cfg file and gets the consumer_key and _secret
config = ConfigParser.RawConfigParser()
config.read('twitterbot.cfg')

consumer_key = config.get('TwitterBot', 'consumer_key')
consumer_secret = config.get('TwitterBot', 'consumer_secret')

# Makes first contact with twitter
twitter = OAuthApi(consumer_key, consumer_secret)

# Get the temporary credentials for our next few calls
temp_credentials = twitter.getRequestToken()

# User pastes this into their browser to bring back a pin number
print '[*] Visit this URL in a web browser and copy the PIN'
print twitter.getAuthorizationURL(temp_credentials)

# Get the pin # from the user and get permanent credentials
oauth_verifier = raw_input('[*] What is the PIN?: ')
access_token = twitter.getAccessToken(temp_credentials, oauth_verifier)

# Sets values in the config file
config.set('TwitterBot', 'oauth_token', access_token['oauth_token'])
config.set('TwitterBot', 'oauth_token_secret', access_token['oauth_token_secret'])
with open('twitterbot.cfg', 'wb') as configfile:
    config.write(configfile)

print '[*] OAuth tokens set!'
