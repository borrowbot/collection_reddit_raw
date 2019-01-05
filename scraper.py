#!/usr/bin/env python

import praw

reddit = praw.Reddit(client_id='EXmKlisPai3bBA', client_secret='M-f_hLb4F3XMSDa1tWIHjQyACMs', password='kj7XRQ%PJ2cb', user_agent='frank_and_yoon', username='lee-y')

subreddit = reddit.subreddit('borrow')

for posts in subreddit.new(limit=10):
	print(posts.title)