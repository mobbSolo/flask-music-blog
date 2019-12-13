""" populate_posts.py
GET timestamp of the latest database entry
COMPARE timestamp with latest youtube channel posting
IF ther is a NEWER upload, ADD to our Database
"""
import os, re, datetime, sqlite3
import dateutil.parser
import googleapiclient.discovery


DATABASE = 'test.db'
CHANNEL_ID = "UC7PGJuACuivUYrMytFvHV6Q" #Dr. Sandpaper Channel


def fetch_videos():
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
        channelId=CHANNEL_ID,
        maxResults=39
    )

    son = request.execute()
    new_post = []


    for each in range(len(son['items'])):
        # chan_name = son['items'][each]['snippet']['channelTitle']
        title = son['items'][each]['snippet']['title'].split(' (')[0]
        link_id = son['items'][each]['contentDetails']['upload']['videoId']
        published = dateutil.parser.parse(
                    son['items'][each]['snippet']['publishedAt']
        )
        time = published.strftime('%Y-%m-%d %H:%M:%S%z')

        post = (title.title(), link_id, time)
        new_post.append(post)
        # print(published <= "2019-11-30T11:58:32.000Z")
        # print()
        # print(title)
        # print(link_id)
        # print(published)
    return new_post


if __name__ == "__main__":
    posts = fetch_videos()
    print(posts)

    with sqlite3.connect(DATABASE) as base:
        curse = base.cursor()
        curse.executemany('''INSERT INTO post(title, link, timestamp)
                            VALUES(?, ?, ?)''', posts)

