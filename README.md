## Personal Music Blog
Simple Flask Blog for posting original music hosted on youtube.. Secretly built for a friend of mine.

---
#### `fetch_new_vids.py`:

* This script (run via cron-job) will check the given youtube channel for new uploads then add them to our database.
* I have a systemd timer run our script twice a day in production.

#### `populate_posts.py`:

* This script is run initially to populate our database with all the videos from a given channel
