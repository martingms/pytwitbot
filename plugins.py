#!/usr/bin/env python
# encoding: utf-8
"""
plugins.py

Written by Martin Gammelsæter (@martingamm)

"""

from oauthtwitter import OAuthApi
import time
import threading

# UptimeTweeter-specific imports
from commands import getoutput

# XMLTweeter-specific imports
from BeautifulSoup import BeautifulStoneSoup
import urllib2

class XMLTweeter(threading.Thread):
    '''
    Author: Martin Gammelsæter (@martingamm)
    Description: Tweets title and link of a XMLfeed, in this example the mac1.no feed
    
    Non-library modules: BeautifulSoup
    '''
    def __init__(self, twitter):
        threading.Thread.__init__(self)
        self.twitter = twitter
    
    def run(self):
        title = ''
        while True:
            url = 'http://mac1.no/node/feed'
            try:
                feed = urllib2.urlopen(url)
                soup = BeautifulStoneSoup(feed, fromEncoding='utf-8')
                titles = soup.findAll('title')
                links = soup.findAll('link')
                #FIXME throws an unicode exception for strings with wierd characters
                title = titles[1].contents[0].string
                link = links[1].contents[0].string
                status = str(title) + ' ' + str(link)
            except:
                print '[*] Unable to fetch from feed.'
            #FIXME don't ruin twitter by spamming requests
            try:
                self.twitter.UpdateStatus(status)
                print '[*] Tweeted the post: ' + title
            except:
                pass
            
            # Sleeps for 3 minutes
            time.sleep(float(180))

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
            
            # Sleeps for an hour...
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
            try:
                friends = self.twitter.GetFriendsIds()
                followers = self.twitter.GetFollowersIds()
                tofollow = list(set(followers) - set(friends))
                #FIXME this does not work as expected, prints every 10 minutes..
                #if tofollow:
                #    print '[*] Trying to follow your followers...'
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
            
            # Sleeps for 10 minutes
            time.sleep(float(600))

# Install plugins by making a variable of the class and putting it in the plugins array
# FIXME fix this ugly hack   
XMLT = XMLTweeter  
UpTweeter = UptimeTweeter
FollowBk = FollowBack
plugins = [XMLT, FollowBk]