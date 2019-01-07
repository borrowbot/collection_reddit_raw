#!/usr/bin/env python
import logging
import praw
import collection_raw_ingest.src.psraw as psraw
import time
from datetime import datetime


reddit = praw.Reddit(client_id='EXmKlisPai3bBA', client_secret='M-f_hLb4F3XMSDa1tWIHjQyACMs', password='kj7XRQ%PJ2cb', user_agent='frank_and_yoon', username='lee-y')
# subreddit = reddit.subreddit('borrow')

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
logger = logging.getLogger('prawcore')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

n = 1
for post in psraw.submission_search(reddit, q='', subreddit='borrow', limit=5000, sort='desc'):
# for post in subreddit.new(limit=10000):
	print("{}:{}: {}".format(n, datetime.fromtimestamp(post.created_utc).strftime('%Y-%m-%d %H:%M:%S'), post.id))
	n += 1
