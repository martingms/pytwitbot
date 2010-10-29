#!/usr/bin/env python
# encoding: utf-8
"""
pytwitbot.py

Written by Martin Gammelsæter (@martingamm)

"""

# Importing non-library modules
from oauthtwitter import OAuthApi
import plugins

# Importing library modules
import ConfigParser
import sys


class TwitterBot(object):
    '''
    The main pytwitbot class
    '''
    def __init__(self):
        self.oauth_token = ''
        self.oauth_token_secret = ''
        self.consumer_key = ''
        self.consumer_secret = ''
        
    
    def readConfig(self):
        '''
        Parses the standard config file "twitterbot.cfg"
        '''
        
        # Opens twitterbot.cfg
        config = ConfigParser.RawConfigParser()
        config.read('twitterbot.cfg')
        
        # Parses the contents of the cfg
        self.oauth_token = config.get('TwitterBot', 'oauth_token')
        self.oauth_token_secret = config.get('TwitterBot', 'oauth_token_secret')
        self.consumer_key = config.get('TwitterBot', 'consumer_key')
        self.consumer_secret = config.get('TwitterBot', 'consumer_secret')
                
    def runBot(self):
        '''
        Runs the bot.
        Reads config, authenticates with twitter and runs main loop.
        '''
        print '[*] Starting up...'
        
        # Tries to read config file, exits program if unable
        print '[*] Trying to read config file...'
        try:
            self.readConfig()
            print '[*] Config successfully parsed!'
        except:
            print '[*] Unable to read config!'
            print '[*] Bot shutting down...'
            sys.exit()
        
        # Tries to authenticate with twitter, exits program if unable
        print '[*] Trying to authenticate with twitter...' 
        try:
            twitter = OAuthApi(self.consumer_key, self.consumer_secret, self.oauth_token, self.oauth_token_secret)
            print '[*] Successfully authenticated with twitter!'
        except:
            print '[*] Unable to authenticate with twitter at this time...'
            print '[*] Bot shutting down...'
            sys.exit()
        
        # Runs every plugin that is installed in a separate thread
        i = 0
        for plugin in plugins.plugins:
            try:
                temp = plugin(twitter)
                temp.start()
                i +=1
            except:
                print '[*] A plugin failed to initialize'
        
        print '[*] ' + str(i) + ' threads running ' + str(i) + ' plugins.'