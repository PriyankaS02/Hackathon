#!/usr/bin/env python
#
# Extracts email addresses from one or more plain text files.
#
# Notes:
# - Does not save to file (pipe the output to a file if you want it saved).
# - Does not check for duplicates (which can easily be done in the terminal).
#
# (c) 2013  Dennis Ideler <ideler.dennis@gmail.com>

from optparse import OptionParser
import os.path
import re
import tweepy
import sys
import os

regex = re.compile(("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                    "{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
                    "\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))

consumer_key='7OvwoX2aKIvMYNllMMwfBkv2O'
consumer_secret='AVe1CGJx2Q9bBeWmH5gkgJB8Lcgmhj2lV7NPxP6iFwd1AuMq8K'
access_token='3233127751-hwP0PgXHXyBK8axKQFZrbbJjuPoD0y9blz2ZKn2'
access_token_secret='uMdG3NIRuFu6Hmbkic1y21QzGXt5c5mNYWLSmSCq2joh4'
name='PriyankaS02'
def file_to_str(filename):
    """Returns the contents of filename as a string."""
    with open(filename) as f:
        return f.read().lower() # Case is lowered to prevent regex mismatches.

def get_emails(s):
    """Returns an iterator of matched emails found in string s."""
    # Removing lines that start with '//' because the regular expression
    # mistakenly matches patterns like 'http://foo@bar.com' as '//foo@bar.com'.
    return (email[0] for email in re.findall(regex, s) if not email[0].startswith('//'))
def suggest_addon():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    public_tweets = api.user_timeline(screen_name=name,count=100)
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    i=0
    keyword_list=[]
    keyword_dict={}
    #create a keywoord lookup
    with open('lookup_keyword.txt','r') as file:
        for line in file:
            keyword_list.append(line)
    print(keyword_list)
    keyword_dict=dict((el.rstrip(),0) for el in keyword_list )
    print(keyword_dict)
    print(len(public_tweets))

    # Process each tweet
    for tweet in public_tweets:
        tweet_text=tweet.text
        print(i,tweet_text.translate(non_bmp_map))
        i=i+1
    for tweet in public_tweets:
        for word in tweet.text.split():
            for key, value in keyword_dict.items():
                if key in word.lower():
                    keyword_dict[key]=value+1
    print(keyword_dict)
    for key, value in keyword_dict.items():
        if value!=0:
            print ('Suggest',key,'add-on')
    
if __name__ == '__main__':
    parser = OptionParser(usage="Usage: python %prog [FILE]...")
    # No options added yet. Add them here if you ever need them.
    options, args = parser.parse_args()

    if not args:
        parser.print_usage()
        exit(1)

    for arg in args:
        if os.path.isfile(arg):
            for email in get_emails(file_to_str(arg)):
                print (email)
        else:
            print ('"{}" is not a file.'.format(arg))
            parser.print_usage()
    suggest_addon()
