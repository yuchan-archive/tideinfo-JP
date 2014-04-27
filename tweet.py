#! /usr/bin/env python
 # -*- coding: utf-8 -*-

from rauth import OAuth1Service, OAuth1Session
import tweepy
import urllib2
import xml.etree.ElementTree as ET
from random import randrange

CONSUMER_KEY=''
CONSUMER_SECRET=''
CREDENTIAL_FILE='./credential.txt'
TEXT_DATE="本日の"
TEXT1='の潮汐情報です。\n'

try:
    read_input = raw_input
except NameError:
    read_input = input

def saveTwitterSession(session):
    f = open(CREDENTIAL_FILE, 'w+')
    f.write(str(session.access_token) + '\n')
    f.write(str(session.access_token_secret) + '\n')
    f.close()


def createAuthSession():
    twitter = OAuth1Service(
        name="twitter",
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        request_token_url='https://api.twitter.com/oauth/request_token',
        access_token_url='https://api.twitter.com/oauth/access_token',
        authorize_url='https://api.twitter.com/oauth/authorize',
        base_url='https://api.twitter.com/1.1/')

    request_token, request_token_secret = twitter.get_request_token()
    authorize_url = twitter.get_authorize_url(request_token)

    print('Visit this URL in your browser: {url}'.format(url=authorize_url))
    pin = read_input('Enter PIN from browser: ')

    try:
        session = twitter.get_auth_session(request_token,
                                   request_token_secret,
                                   method='POST',
                                   data={'oauth_verifier': pin})
        
        return session
    except KeyError:
        print pin + " is not valid pin number."
        return None

def retreiveSession():
    f = open(CREDENTIAL_FILE,'r')
    token = ""
    secret = ""
    count = 0
    for line in f:
        if count == 0:
            token = line.strip()
        else:
            secret = line.strip()

        count += 1

    try:
        if len(token) <= 0 or len(secret) <= 0:
            raise KeyError

        session = OAuth1Session(
                CONSUMER_KEY,
                CONSUMER_SECRET,
                access_token=token,
                access_token_secret=secret)
        return session
    except KeyError:
        return None

def twitterapi(session):
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(session.access_token, session.access_token_secret)
    saveTwitterSession(session)
    return tweepy.API(auth)

def getTideInfo(areaName):
    url = "http://www.e-tsuri.info/tide?p={spot}&d=today".format(spot=unicode(areaName, "utf-8").encode('utf-8'))
    response = urllib2.urlopen(url)
    root = ET.fromstring(response.read())
    return root


def updateTideInfo():
    session = retreiveSession()
    if session == None or session.access_token == None or session.access_token_secret == None:
        session = createAuthSession()
   
    api = twitterapi(session)
    
    with open('./ports.txt') as f:
        contents = f.readlines()
        num = len(contents)
        rand = randrange(num)
        info = getTideInfo(contents[rand].strip())
        tweetinfo = ""
        latValue = ""
        longValue = ""

        for child in info:
            if child.tag == 'tide':
                tweetinfo = TEXT_DATE + contents[rand].strip() + TEXT1 + child.text
            elif child.tag == 'lat':
                latValue = child.text
            elif child.tag == 'lng':
                longValue = child.text

        api.update_status(tweetinfo, lat=latValue, long=longValue)


def main():
    updateTideInfo()

if __name__ == "__main__":
    main()

