# -*- coding: utf-8 -*-

import os
import sys
import twitter

from twitter.oauth import write_token_file, read_token_file
from twitter.oauth_dance import oauth_dance

def oauth_login(app_name='',
                consumer_key='', 
                consumer_secret='', 
                token_file='out/twitter.oauth'):

    try:
        (access_token, access_token_secret) = read_token_file(token_file)
    except IOError, e:
        (access_token, access_token_secret) = oauth_dance(app_name, consumer_key,
                                                          consumer_secret)

        if not os.path.isdir('out'):
            os.mkdir('out')

        write_token_file(token_file, access_token, access_token_secret)

        print >> sys.stderr, "OAuth Success. Token file stored to", token_file

    return twitter.Twitter(domain='api.twitter.com', api_version='1',
                           auth=twitter.oauth.OAuth(access_token, access_token_secret,
                                                    consumer_key, consumer_secret))

def read_oauth_file(filename):
    f = open(filename)
    return f.readline().strip(), f.readline().strip(),\
        f.readline().strip(), f.readline().strip()

def login(filename='twitter-oauth.txt'):
    (access_token, access_token_secret, consumer_key, consumer_secret) = \
        read_oauth_file(filename)
    auth = twitter.oauth.OAuth(access_token, access_token_secret,
                               consumer_key, consumer_secret)
    return twitter.Twitter(domain='api.twitter.com', api_version='1',
                           auth=auth)

if __name__ == '__main__':

    # Go to http://twitter.com/apps/new to create an app and get these items
    # See also http://dev.twitter.com/pages/oauth_single_token

    APP_NAME = ''
    CONSUMER_KEY = ''
    CONSUMER_SECRET = ''

    oauth_login(APP_NAME, CONSUMER_KEY, CONSUMER_SECRET, 'twitter.oauth')
