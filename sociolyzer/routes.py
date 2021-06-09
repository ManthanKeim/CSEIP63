from flask import Flask, render_template, request
import pandas as pd
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from sociolyzer.scraper import get_tweets_max,get_tweets,youtube_comments
#from sociolyzer.visu import visualizations
from sociolyzer.preprocessing import process_text
from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup
import geocoder
import gmplot
import os
import re
app = Flask(__name__)
REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
STOPWORDS = set(stopwords.words('english'))
def clean_text(text):
    text = BeautifulSoup(text, "lxml").text
    text = text.lower()
    text = REPLACE_BY_SPACE_RE.sub(' ', text)
    text = BAD_SYMBOLS_RE.sub('', text)
    text = ' '.join(word for word in text.split() if word not in STOPWORDS)
    return text

@app.route("/")
def index():
    return render_template("landing.html")


@app.route("/dash", methods=['GET','POST'])
def dash():
    try:
        query = request.form.get("query")
        option = request.form.get("options")
        pos_sent=neg_sent=neu_sent=0
        
        if(option == "Twitter Latest/Mixed"):
            tweets = get_tweets(query)
            tweets_df = pd.read_csv("saved_tweets.csv")
#            visualizations(tweets_df)
            #uncomment for map
#            coordinates = {'latitude': [], 'longitude': []}
#            for count, user_loc in enumerate(tweets_df.location):
#                try:
#                    if(user_loc.isspace()):
#                        print("true")
#                    location = geocoder.arcgis(user_loc)
#
#                    # If coordinates are found for location
#                    if location:
#                        coordinates['latitude'].append(location.y)
#                        coordinates['longitude'].append(location.x)
#
#                # If too many connection requests
#                except:
#                    pass
#
#            # Instantiate and center a GoogleMapPlotter object to show our map
#            gmap = gmplot.GoogleMapPlotter(30, 0, 3,apikey="AIzaSyC0yld0y8Ic_rJ_Jip5EdY3iQr-UrfRR1c")
#            # Insert points on the map passing a list of latitudes and longitudes
#            gmap.heatmap(coordinates['latitude'], coordinates['longitude'], radius=20)
#            #
#            ## Save the map to html file
#            gmap.draw("sociolyzer/static/css/python_heatmap.html")
            
            
            tweets_text = list(tweets_df['text'])
            total_tweets = len(tweets_df)
            total_retweets = tweets_df['retweets'].sum()
            total_likes = tweets_df['likes'].sum()
            responses = process_text(tweets_text, query)
            styles = ["primary", "success", "info", "warning", "danger", "secondary"]
            
            # sentiment analysis
            tweets_df['text2']=tweets_df['text'].apply(clean_text)
            tweets_df['sentiment'] = tweets_df['text2'].apply(lambda x: TextBlob(x).sentiment.polarity)
            for i in tweets_df['sentiment']:
                if(i>0):
                    pos_sent+=1
                elif(i<0):
                    neg_sent+=1
                elif(i==0):
                    neu_sent+=1
            print(pos_sent,neg_sent,neu_sent)
            # sort tweets by likes then retweets and get the top 6 tweets
            tweets_df = tweets_df.sort_values(['retweets', 'likes'], ascending=False)
            tweets_df = tweets_df.drop_duplicates('text')
            tweets_df['text'] = tweets_df['text'].apply(lambda x: x.strip())
            top_tweets = tweets_df.iloc[:3, :].to_dict("records")
            os.remove("saved_tweets.csv")

            return render_template("dashboard.html", text1="Twitter",text2="Tweets",text3="Retweets",text4="Likes",text5="Tweets", query=query, total_tweets=total_tweets, icon1="fab fa-twitter fa-2x text-gray-300",icon2="fas fa-retweet fa-2x text-gray-300",icon3="fas fa-heart fa-2x text-gray-300",
            total_retweets=total_retweets, total_likes=total_likes, hashtags=zip(responses['hashtags'], styles),
             cloud_sign=responses['cloud_sign'], negative_counts=neg_sent, positive_counts=pos_sent, neutral_counts=neu_sent, top_tweets=top_tweets)
             
             
        elif(option == "Twitter Stream"):
            tweets = get_tweets_max(query,max_tweets=500)
            tweets_df = pd.read_csv("saved_tweets.csv")
#            visualizations(tweets_df)
            #uncomment for map
#            coordinates = {'latitude': [], 'longitude': []}
#            for count, user_loc in enumerate(tweets_df.location):
#                try:
#                    if(user_loc.isspace()):
#                        print("true")
#                    location = geocoder.arcgis(user_loc)
#
#                    # If coordinates are found for location
#                    if location:
#                        coordinates['latitude'].append(location.y)
#                        coordinates['longitude'].append(location.x)
#
#                # If too many connection requests
#                except:
#                    pass
#
#            # Instantiate and center a GoogleMapPlotter object to show our map
#            gmap = gmplot.GoogleMapPlotter(30, 0, 3,apikey="AIzaSyC0yld0y8Ic_rJ_Jip5EdY3iQr-UrfRR1c")
#            # Insert points on the map passing a list of latitudes and longitudes
#            gmap.heatmap(coordinates['latitude'], coordinates['longitude'], radius=20)
#            #
#            ## Save the map to html file
#            gmap.draw("sociolyzer/static/css/python_heatmap.html")
            
            
            tweets_text = list(tweets_df['text'])
            total_tweets = len(tweets_df)
            total_retweets = tweets_df['retweets'].sum()
            total_likes = tweets_df['likes'].sum()
            responses = process_text(tweets_text, query)
            styles = ["primary", "success", "info", "warning", "danger", "secondary"]

            # sentiment analysis
            tweets_df['text2']=tweets_df['text'].apply(clean_text)
            tweets_df['sentiment'] = tweets_df['text2'].apply(lambda x: TextBlob(x).sentiment.polarity)
            for i in tweets_df['sentiment']:
                if(i>0):
                    pos_sent+=1
                elif(i<0):
                    neg_sent+=1
                elif(i==0):
                    neu_sent+=1
            print(pos_sent,neg_sent,neu_sent)
            # sort tweets by likes then retweets and get the top 6 tweets
            tweets_df = tweets_df.sort_values(['retweets', 'likes'], ascending=False)
            tweets_df = tweets_df.drop_duplicates('text')
            tweets_df['text'] = tweets_df['text'].apply(lambda x: x.strip())
            top_tweets = tweets_df.iloc[:3, :].to_dict("records")
            os.remove("saved_tweets.csv")

            return render_template("dashboard.html", text1="Twitter",text2="Tweets",text3="Retweets",text4="Likes",text5="Tweets",query=query, total_tweets=total_tweets, icon1="fab fa-twitter fa-2x text-gray-300",icon2="fas fa-retweet fa-2x text-gray-300",icon3="fas fa-heart fa-2x text-gray-300",
            total_retweets=total_retweets, total_likes=total_likes, hashtags=zip(responses['hashtags'], styles),
             cloud_sign=responses['cloud_sign'], negative_counts=neg_sent, positive_counts=pos_sent, neutral_counts=neu_sent, top_tweets=top_tweets)
            
            
            
            
        elif(option == "Youtube"):
            youtube_comments(query)
            tweets_df = pd.read_csv("saved_tweets.csv")
#            visualizations(tweets_df)
            tweets_text = list(tweets_df['text'])
            total_tweets = tweets_df['comments'][1]
            total_retweets = tweets_df['likes_count'][1]
            total_likes = tweets_df['dislikes'][1]
            responses = process_text(tweets_text, query)
            styles = ["primary", "success", "info", "warning", "danger", "secondary"]
            
            # sentiment analysis
            tweets_df['text2']=tweets_df['text'].apply(clean_text)
            tweets_df['sentiment'] = tweets_df['text2'].apply(lambda x: TextBlob(x).sentiment.polarity)
            for i in tweets_df['sentiment']:
                if(i>0):
                    pos_sent+=1
                elif(i<0):
                    neg_sent+=1
                elif(i==0):
                    neu_sent+=1
            print(pos_sent,neg_sent,neu_sent)
            # sort tweets by likes then retweets and get the top 6 tweets
            tweets_df = tweets_df.sort_values(['retweets', 'likes'], ascending=False)
            tweets_df = tweets_df.drop_duplicates('text')
            tweets_df['text'] = tweets_df['text'].apply(lambda x: x.strip())
            top_tweets = tweets_df.iloc[:3, :].to_dict("records")
            os.remove("saved_tweets.csv")

            return render_template("dashboard.html", text1="Youtube",text2="Comments",text3="Likes",text4="Dislikes",text5="Comments", query=query, total_tweets=total_tweets, icon1="fas fa-comments fa-2x text-gray-300",icon2="fas fa-thumbs-up fa-2x text-gray-300",icon3="fas fa-thumbs-down fa-2x text-gray-300",
            total_retweets=total_retweets, total_likes=total_likes, hashtags=zip(responses['hashtags'], styles),
             cloud_sign=responses['cloud_sign'], negative_counts=neg_sent, positive_counts=pos_sent, neutral_counts=neu_sent, top_tweets=top_tweets)
    except Exception as e:
        print(e)
        return render_template("error.html")
