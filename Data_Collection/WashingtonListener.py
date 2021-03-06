import time
import json
import sys
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from pymongo import MongoClient
from keys import *

# keys
start_time = time.time()  # grabs the system time
keyword_list = ['twitter']  # track list
ckey = consumer_key
consumer_secret = consumer_secret
access_token_key = access_token
access_token_secret = access_token_secret


class listener(StreamListener):
    def __init__(self, start_time, time_limit=82800):

        self.time = start_time
        self.limit = time_limit
        self.tweet_data = []

    def on_data(self, status):
        while (time.time() - self.time) < self.limit:
            tweet = json.loads(status)
            try:
                client = MongoClient('localhost', 27017)
                db = client['Washington_tweets']
                collection = db['twitter_collection']
                if tweet['coordinates'] is not None:
                    collection.insert(tweet)
                return True
            # various exception handling blocks
            except KeyboardInterrupt:
                sys.exit()
            except AttributeError as e:
                print('AttributeError was returned, stupid bug')
                print(e)
            except tweepy.TweepError as e:
                print('Below is the printed exception')
                print(e)
                if '401' in e:
                    # not sure if this will even work
                    print('Below is the response that came in')
                    print(e)
                    time.sleep(60)
                else:
# raise an exception if another status code was returned,we don't like other kinds
                    time.sleep(60)
            except BaseException as e:
                print('failed ondata,', str(e))
                time.sleep(5)
        exit()

    def on_error(self, status):
        print(status)
# Instance
auth = OAuthHandler(ckey, consumer_secret)  # Consumer keys
auth.set_access_token(access_token_key, access_token_secret)  # Secret Keys
# initialize Stream object with a time out limit
twitterStream = Stream(auth, listener(start_time, time_limit=82800))
# bounding box filter for Washington
twitterStream.filter(locations=[-124.84, 45.54, -116.92, 49.0])
