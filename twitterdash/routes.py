from flask import Flask, render_template, request
import pandas as pd
from textblob import TextBlob
from twitterdash.scraper import get_tweets_max,get_tweets
from twitterdash.preprocessing import process_text
from geopy.geocoders import Nominatim
import geocoder
import gmplot
import os
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("landing.html")


@app.route("/dash", methods=['GET','POST'])
def dash():
    query = request.form.get("query")
    option = request.form.get("options")
    if(option == "Twitter Latest/Mixed"):
        tweets = get_tweets(query)
    elif(option == "Twitter Stream"):
        tweets = get_tweets_max(query,max_tweets=500)
    elif(option == "Youtube"):
        print("To be decided")
#    columns = ['fullname', 'is_retweet', 'likes',
#               'replies', 'retweet_id', 'retweeter_userid', 'retweeter_username', 'retweets',
#               'text', 'timestamp', 'tweet_id', 'user_id', 'username', 'tweet_url']
#    tweets_df = pd.DataFrame(columns=columns)
#
#    for tweet in tweets:
#        tweet_dict = {}
#        for att in columns:
#            tweet_dict[att] = getattr(tweet, att)
#        tweets_df = tweets_df.append(tweet_dict, ignore_index=True)
    tweets_df = pd.read_csv("saved_tweets.csv")
    
    #uncomment for map
    coordinates = {'latitude': [], 'longitude': []}
    for count, user_loc in enumerate(tweets_df.location):
        try:
            if(user_loc.isspace()):
                print("true")
            location = geocoder.arcgis(user_loc)

            # If coordinates are found for location
            if location:
                print(location)
                coordinates['latitude'].append(location.y)
                coordinates['longitude'].append(location.x)

        # If too many connection requests
        except:
            pass

    # Instantiate and center a GoogleMapPlotter object to show our map
    gmap = gmplot.GoogleMapPlotter(30, 0, 3,apikey="AIzaSyC0yld0y8Ic_rJ_Jip5EdY3iQr-UrfRR1c")
    # Insert points on the map passing a list of latitudes and longitudes
    gmap.heatmap(coordinates['latitude'], coordinates['longitude'], radius=20)
    #
    ## Save the map to html file
    gmap.draw("twitterdash/static/css/python_heatmap.html")
#
    
    
    
    tweets_text = list(tweets_df['text'])
    total_tweets = len(tweets_df)
    total_retweets = tweets_df['retweets'].sum()
    total_likes = tweets_df['likes'].sum()
    responses = process_text(tweets_text, query)
    styles = ["primary", "success", "info", "warning", "danger", "secondary"]

    # sentiment analysis
    tweets_df['sentiment'] = tweets_df['text'].apply(lambda x: TextBlob(x).sentiment.polarity.is_integer())
    sentiment = tweets_df['sentiment'].value_counts()
    pos_sent = sentiment[True]
    neg_sent = sentiment[False]

    # sort tweets by likes then retweets and get the top 6 tweets
    tweets_df = tweets_df.sort_values(['retweets', 'likes'], ascending=False)
    tweets_df = tweets_df.drop_duplicates('text')
    tweets_df['text'] = tweets_df['text'].apply(lambda x: x.strip())
    top_tweets = tweets_df.iloc[:3, :].to_dict("records")
    os.remove("saved_tweets.csv")

    return render_template("dashboard.html", query=query, total_tweets=total_tweets,
    total_retweets=total_retweets, total_likes=total_likes, hashtags=zip(responses['hashtags'], styles),
     cloud_sign=responses['cloud_sign'], negative_counts=neg_sent, positive_counts=pos_sent, top_tweets=top_tweets)
