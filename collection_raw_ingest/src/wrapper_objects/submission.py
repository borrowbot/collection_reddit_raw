import time
from datetime import datetime


class Submission(object):
    def __init__(self, praw_submission):
        self.praw_submission = praw_submission

        self.submission_id = self.praw_submission.id
        self.creation_datetime = datetime.utcfromtimestamp(self.praw_submission.created_utc)
        self.retrieval_datetime = datetime.utcnow()
        self.score = self.praw_submission.score
        self.num_comments = self.praw_submission.num_comments
        self.permalink = self.praw_submission.permalink
        self.subreddit_name = self.praw_submission.subreddit
        self.subreddit_id = self.praw_submission.subreddit.name
        self.title = self.praw_submission.title
        self.text = self.praw_submission.selftext

        # Try/except blocks to cover deleted authors
        try:
            self.author_name = self.praw_submission.author.name
        except:
            self.author_name = None
        try:
            self.author_id = self.praw_submission.author_fullname
        except:
            self.author_id = None
