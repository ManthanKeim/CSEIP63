# -*- coding: utf-8 -*-

# Sample Python code for youtube.commentThreads.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import googleapiclient.discovery
import pandas as pd

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyC0yld0y8Ic_rJ_Jip5EdY3iQr-UrfRR1c"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)
    nextPageToken = ""
    videoId = input("Link of YT video:")
    videoId = videoId[32:]
    request = youtube.videos().list(
        part="statistics",
        id=videoId
    )
    response = request.execute()
    response = response["items"][0]["statistics"]
    print("Views :" + response["viewCount"])
    print("Likes :" + response["likeCount"])
    print("Dislikes :" + response["dislikeCount"])
    print("Comments :" + response["commentCount"])
    dict_ = {'date/time': [], 'comment_id':[],'fullname': [],'text': [], 'likes': [], 'replyComment count':[]}
    for i in range(10):
        request = youtube.commentThreads().list(
            part="snippet",
            maxResults=100,
            order="relevance",
            pageToken=nextPageToken,
            textFormat="plainText",
            videoId=videoId
        )
        response = request.execute()
        nextPageToken = response["nextPageToken"]
        commentArray = response["items"]
        for i in commentArray:
             dict_['date/time'].append(i["snippet"]["topLevelComment"]["snippet"]["publishedAt"])
             dict_['comment_id'].append(i["snippet"]["topLevelComment"]["id"])
             dict_['fullname'].append(i["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"])
             dict_['text'].append(i["snippet"]["topLevelComment"]["snippet"]["textOriginal"])
             dict_['likes'].append(i["snippet"]["topLevelComment"]["snippet"]["likeCount"])
             dict_['replyComment count'].append(i["snippet"]["totalReplyCount"])
    df = pd.DataFrame(dict_)
    df.to_csv('yt_comments.csv',index=False)
if __name__ == "__main__":
    main()