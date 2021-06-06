from datetime import datetime, date, timedelta
#from twitterscraper import query_tweets
from collections import Counter
import ast
import pandas as pd
import json
from dotenv import load_dotenv
from twython import Twython
from twython import TwythonStreamer
import os
import csv
import googleapiclient.discovery
load_dotenv()
credentials = {}
credentials['CONSUMER_KEY'] = os.getenv("TWITTER_API_KEY")
credentials['CONSUMER_SECRET'] = os.getenv("TWITTER_API_SECRET")
credentials['ACCESS_TOKEN'] = os.getenv("TWITTER_ACCESS_TOKEN")
credentials['ACCESS_SECRET'] = os.getenv("TWITTER_ACESSS_TOKEN_SECRET")

python_tweets = Twython(credentials['CONSUMER_KEY'], credentials['CONSUMER_SECRET'])


def get_tweets(query):
    query1 = {'q': query,
            'result_type': 'mixed',
            'count': 2000,
            'lang': 'en',
            }

    dict_ = {'date': [],'url':[], 'tweet_id':[],'fullname': [],'user_id':[],'text': [],'hashtags':[], 'likes': [], 'retweets':[], 'location':[]}
    for status in python_tweets.search(**query1, tweet_mode='extended')['statuses']:
        dict_['fullname'].append(status['user']['screen_name'])
        dict_['url'].append(i for i in status['entities']['urls'])
        dict_['tweet_id'].append(status['id_str'])
        dict_['user_id'].append(status['user']['name'])
        dict_['date'].append(status['created_at'])
        dict_['text'].append(status['full_text'])
        dict_['hashtags'].append([hashtags['text'] for hashtags in status['entities']['hashtags']])
        dict_['likes'].append(status['favorite_count'])
        dict_['retweets'].append(status['retweet_count'])
        dict_['location'].append(status['user']['location'])
    #
    ## Structure data in a pandas DataFrame for easier manipulation
    df = pd.DataFrame(dict_)
    df.to_csv('saved_tweets.csv',index=False)
    #df.sort_values(by='favorite_count', inplace=True, ascending=False)
#    print(dict_)

#def process_tweet(tweet):
##    result = geocoder.arcgis(tweet['user']['location'])
#    d = {}
#    d['created_at'] = tweet['created_at']
##    d['url'] = tweet['retweeted_status']['entities']['urls'][0]['url']
#    d['hashtags'] = [hashtags['text'] for hashtags in tweet['entities']['hashtags']]
#    d['text'] = tweet['text']
#    d['user'] = tweet['user']['screen_name']
#    d['user_loc'] = tweet['user']['location']
#    d['fullname'] = tweet['user']['name']
#    d['likes'] = tweet['favorite_count']
#    d['retweets'] = tweet['retweet_count']
#
#    return d
#
#
## Create a class that inherits TwythonStreamer
#class MyStreamer(TwythonStreamer):
#    max_tweets = 1000
#    count=0
#    # Received data
#    def on_success(self, data):
#        # Only collect tweets in English
#        if data['lang'] == 'en':
#            count+=1
#            tweet_data = process_tweet(data)
#            self.save_to_csv(tweet_data)
#            if (count >= max_tweets):
#              self.disconnect()
#              return False
#
#    # Problem with the API
#    def on_error(self, status_code, data):
#        print(status_code, data)
#        self.disconnect()
#
#    # Save each tweet to csv file
#    def save_to_csv(self, tweet):
#        with open(r'saved_tweetseam.csv', 'a') as file:
#            writer = csv.writer(file)
#            writer.writerow(list(tweet.values()))



dict_header = ['fullname','url', 'tweet_id','user_id','date','text','hashtags', 'likes', 'retweets', 'location']
#with open(r'saved_tweets.csv', 'a') as file:
#    writer = csv.DictWriter(file, fieldnames=dict_header)
def process_tweet(status):
    dict_ = {'fullname': [],'url':[], 'tweet_id':[],'user_id': [],'date':[],'text': [],'hashtags':[], 'likes': [], 'retweets':[], 'location':[]}
    dict_['user_id']=(status['user']['screen_name'])
    dict_['tweet_id']=(status['id_str'])
    dict_['fullname']=(status['user']['name'])
    dict_['date']=(status['created_at'])
    dict_['text']=(status['text'])
    dict_['hashtags']=([hashtags['text'] for hashtags in status['entities']['hashtags']])
    try:
        dict_['likes']=(status['retweeted_status']['favorite_count'])
    except KeyError:
        dict_['likes']=(status['favorite_count'])
    try:
            dict_['retweets']=(status['retweeted_status']['retweet_count'])
    except KeyError:
        dict_['retweets']=(status['retweet_count'])
    dict_['location']=(status['user']['location'])
    dict_['url']="https://twitter.com/"+ dict_['user_id']+ "/status/" + dict_['tweet_id']
    return dict_
    
# Create a class that inherits TwythonStreamer
class MyStreamer(TwythonStreamer):
    tweet_limit=500
    # Received data
    def on_success(self, data):
        MyStreamer.tweet_limit-=1
        # Only collect tweets in English
        if data['lang'] == 'en':
            tweet_data = process_tweet(data)
            self.save_to_csv(tweet_data)
            print(MyStreamer.tweet_limit)
            if(MyStreamer.tweet_limit<=0):
                self.disconnect()

    # Problem with the API
#    def on_error(self, status_code, data):
#        print(status_code, data)
#        self.disconnect()
        
    # Save each tweet to csv file
    def save_to_csv(self, tweet):
        if os.path.isfile('saved_tweets.csv'):
            with open('saved_tweets.csv', 'a', newline='') as my_file:
                w = csv.DictWriter(my_file, fieldnames= dict_header)
                w.writerow(tweet)
        else:
            with open('saved_tweets.csv', 'w', newline='') as my_file:
                w = csv.DictWriter(my_file, fieldnames= dict_header)
                w.writeheader()
                w.writerow(tweet)
            
            
def get_tweets_max(query,max_tweets=500):
    stream = MyStreamer(credentials['CONSUMER_KEY'], credentials['CONSUMER_SECRET'],
                    credentials['ACCESS_TOKEN'], credentials['ACCESS_SECRET'])
    MyStreamer.tweet_limit= max_tweets
    # Start the stream
    try:
        stream.statuses.filter(track=query, tweet_mode='extended')
    except TypeError:
        pass
    








##tweets.head()
#
#list_hashtag_strings = [entry for entry in tweets.hashtags]
#list_hashtag_lists = ast.literal_eval(','.join(list_hashtag_strings))
#hashtag_list = [ht.lower() for list_ in list_hashtag_lists for ht in list_]
#
## Count most common hashtags
#counter_hashtags = Counter(hashtag_list)
#counter_hashtags.most_common(20)
#
#
#
#tweets = pd.read_csv("saved_tweets.csv")



def youtube_comments(query):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = os.getenv("YOUTUBE_API")

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)
#    nextPageToken = "temp"
    videoId = query.split("=")[-1]
    request = youtube.videos().list(
        part="statistics",
        id=videoId
    )
    response = request.execute()
    print(response)
    response = response["items"][0]["statistics"]
    print("Views :" + response["viewCount"])
    print("Likes :" + response["likeCount"])
    print("Dislikes :" + response["dislikeCount"])
    print("Comments :" + response["commentCount"])
    dict_ = {'date': [], 'comment_id':[],'fullname': [],'text': [], 'likes': [], 'retweets':[]}
    for i in range(10):
        request = youtube.commentThreads().list(
            part="snippet",
            maxResults=100,
            order="relevance",
#            pageToken=nextPageToken,
            textFormat="plainText",
            videoId=videoId
        )
        response = request.execute()
#        nextPageToken = response["nextPageToken"]
        commentArray = response["items"]
        for i in commentArray:
             dict_['date'].append(i["snippet"]["topLevelComment"]["snippet"]["publishedAt"])
             dict_['comment_id'].append(i["snippet"]["topLevelComment"]["id"])
             dict_['fullname'].append(i["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"])
             dict_['text'].append(i["snippet"]["topLevelComment"]["snippet"]["textOriginal"])
             dict_['likes'].append(i["snippet"]["topLevelComment"]["snippet"]["likeCount"])
             dict_['retweets'].append(i["snippet"]["totalReplyCount"])
    df = pd.DataFrame(dict_)
    df.to_csv('saved_tweets.csv',index=False)

#youtube_comments("https://www.youtube.com/watch?v=W5NgXKe4SJk")

#def get_last_month_tweets(query, limit=1000, lang="en"):
#    start_date = date.today() - timedelta(30)
#    tweets = query_tweets(query, limit,poolsize=5, lang=lang, begindate=start_date)
#    print(f"got {len(tweets)} tweet.")
#    return tweets
#
#def get_last_half_year_tweets(query, limit=1000, lang="en"):
#    start_date = date.today() - timedelta(30*6)
#    tweets = query_tweets(query, limit,poolsize=5, lang=lang, begindate=start_date)
#    print(f"got {len(tweets)} tweet.")
#    return tweets

#get_last_month_tweets('india')
