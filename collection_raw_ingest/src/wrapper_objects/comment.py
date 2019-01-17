import time
from datetime import datetime


class Comment(object):
    def __init__(self, praw_comment):
        self.praw_comment = praw_comment

        self.comment_id = 't1_' + self.praw_comment.id
        self.creation_datetime = datetime.utcfromtimestamp(self.praw_comment.created_utc)
        self.retrieval_datetime = datetime.utcnow()
        self.score = self.praw_comment.score
        self.subreddit_name = self.praw_comment.subreddit
        self.subreddit_id = self.praw_comment.subreddit.name
        self.link_id = self.praw_comment.link_id
        self.parent_id = self.praw_comment.parent_id
        self.text = self.praw_comment.body

        # Try/except blocks to cover deleted authors
        try:
            self.author_name = self.praw_comment.author.name
        except:
            self.author_name = None
        try:
            self.author_id = self.praw_comment.author_fullname
        except:
            self.author_id = None
