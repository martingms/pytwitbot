#!/usr/bin/env python
# encoding: utf-8
"""
plugins.py

Written by Martin Gammelsæter (@martingamm)

"""

from oauthtwitter import OAuthApi
import time
import threading

# UptimeTweeter-specific import
from commands import getoutput

class UptimeTweeter(threading.Thread):
    '''
    Author: Martin Gammelsæter (@martingamm)
    Description: Tweets the uptime of the machine running the bot every hour
    '''
    def __init__(self, twitter):
        threading.Thread.__init__(self)
        self.twitter = twitter
        
    def run(self):
        while True:
            try:
                uptime = getoutput('uptime')
                self.twitter.UpdateStatus(uptime)
                print '[*] Tweeted the systems uptime.'
            except:
                print '[*] Unable to tweet uptime...'
            
            time.sleep(float(3600))
        
class FollowBack(threading.Thread):
    '''
    Author: Martin Gammelsæter (@martingamm)
    Description: Follows everyone following you
    '''
    def __init__(self, twitter):
        threading.Thread.__init__(self)
        self.twitter = twitter
        
    def run(self):
        while True:
            print '[*] Trying to follow your followers...'
            try:
                friends = self.twitter.GetFriendsIds()
                followers = self.twitter.GetFollowersIds()
                tofollow = list(set(followers) - set(friends))
            except:
                print '[*] Unable to get follow lists...'
                
            try:
                for id in tofollow:
                    try:
                        self.twitter.FollowUser(int(id))
                        print '[*] Now following user id: ' + str(id)
                    except:
                        print '[*] Unable to follow user id: ' + str(id)
            except:
                pass
            
            time.sleep(float(600))

# Install plugins by making a variable of the class and putting it in the plugins array
# FIXME fix this ugly hack      
UpTweeter = UptimeTweeter
FollowBk = FollowBack
plugins = [UpTweeter, FollowBk]