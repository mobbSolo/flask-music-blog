"""
GET timestamp of the latest database entry
COMPARE timestamp with latest youtube channel posting
IF ther is a NEWER upload, ADD to our Database
"""
import os, json, sqlite3, datetime
import dateutil.parser
import googleapiclient.discovery
from dateutil.relativedelta import *


DATABASE = 'songs.db'
CHANNEL_ID = "UC7PGJuACuivUYrMytFvHV6Q" #Dr. Sandpaper Channel


def fetch_last_timestamp(data):
    """Get the timestamp of the last post
       in our database"""
    with sqlite3.connect(data) as base:
        curse = base.cursor()
        curse.execute("""SELECT * FROM post
                        ORDER BY timestamp DESC LIMIT 1;""")
        row = curse.fetchone()
        # Return a datetime object from timestamp
        return dateutil.parser.parse(row[4])



def fetch_new_video(last_pub):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = os.environ.get('FLASK_DEBUG')

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = os.environ.get('GOOGLE_API_KEY') # WOOOPS! KEY-CHANGED

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    request = youtube.activities().list(
        part="snippet,contentDetails",
        channelId=CHANNEL_ID,
        maxResults=5,
        publishedAfter=last_pub.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    )

    son = request.execute()
    new_post =[]

    if len(son['items']) < 1:
        return 'No new uploads'
    else:

        print('Adding to Database:')
        for each in range(len(son['items'])):
            # chan_name = son['items'][each]['snippet']['channelTitle']
            title = son['items'][each]['snippet']['title'].split('(')[0]
            link_id = son['items'][each]['contentDetails']['upload']['videoId']
            published = dateutil.parser.parse(
                        son['items'][each]['snippet']['publishedAt']
            )
            time = published.strftime('%Y-%m-%d %H:%M:%S%z')

            post = (title.title(), link_id, time)
            new_post.append(post)
            # print(published <= "2019-11-30T11:58:32.000Z")
            print()
            print(title)
            print(link_id)
            print(published)

    return new_post


if __name__ == "__main__":
    print('##  ' + str(fetch_last_timestamp(DATABASE)))
    LATEST_VIDEO = fetch_last_timestamp(DATABASE)+relativedelta(minutes=+1)
    print('##  LATEST_VIDEO time: ' + str(LATEST_VIDEO))
    print('---------------------------------------------')
    posts = fetch_new_video(LATEST_VIDEO)

    if posts == 'No new uploads':
        print(posts + ' Nothing added')
    else:
        with sqlite3.connect(DATABASE) as base:
            curse = base.cursor()
            curse.executemany('''INSERT INTO post(title, link, timestamp)
                                VALUES(?, ?, ?)''', posts)

