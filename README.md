## Personal Music Blog
Auto-blog for posting original music hosted on youtube.. Secretly built for a friend of mine.
Later too support posts from other content providers.

---
#### `fetch_new_vids.py`:

* This script will check the given youtube channel for new uploads then add them to our database.
* I have a systemd timer run our script twice a day in production.

#### `populate_posts.py`:

* This script is run initially to populate our database with all the videos from a given channel
