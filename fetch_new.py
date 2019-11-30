#! /usr/bin/python

"""
GET timestamp of the latest database entry
COMPARE timestamp with latest youtube channel posting
IF ther is a NEWER upload, ADD to our Database
"""

import os
import json
import sqlite3
import googleapiclient.discovery



def fetch_last_timestamp(data):
    """Get the timestamp of the last post
       in our database"""
    with sqlite3.connect(data) as base:
        curse = base.cursor()
        curse.execute("""SELECT * FROM post ORDER BY timestamp DESC LIMIT 1;""")
        row = curse.fetchone()
        return row[4]



def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = os.environ.get('GOOGLE_API_KEY') # WOOOPS! KEY-CHANGED

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    request = youtube.activities().list(
        part="snippet,contentDetails",
        channelId="UC7PGJuACuivUYrMytFvHV6Q",
        maxResults=8,
        # publishedAfter="2019-11-21T15:54:33.000Z"
        publishedAfter=LATEST_VIDEO
    )

    son = request.execute()
    if not son:
        print('No new uploads')
    else:

        total_vids = len(son['items'])

        chan_name = son['items'][0]['snippet']['channelTitle']
        published = son['items'][0]['snippet']['publishedAt']
        title = son['items'][0]['snippet']['title']
        idee = son['items'][0]['contentDetails']['upload']['videoId']

        print(str(total_vids) + ' New Videos in ' + chan_name + ' Channel')
        print()
        print(published)
        print(title)
        print(idee)



if __name__ == "__main__":
    LATEST_VIDEO = fetch_last_timestamp('app.db')
    main()
