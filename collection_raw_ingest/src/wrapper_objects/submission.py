from datetime import datetime


class Submission(object):
    def __init__(self, praw_submission):
        self.praw_submission = praw_submission

        self.submission_id = self.praw_submission.id
        self.creation_datetime = datetime.fromtimestamp(self.praw_submission.created_utc)
        self.retrieval_datetime = datetime.fromtimestamp(self.praw_submission.retrieved_on)
        self.score = self.praw_submission.score
        self.num_comments = self.praw_submission.num_comments
        self.author_name = self.praw_submission.author.name
        self.author_id = self.praw_submission.author_fullname
        self.permalink = self.praw_submission.permalink
        self.subreddit_name = self.praw_submission.subreddit
        self.subreddit_id = self.praw_submission.subreddit.name
        self.title = self.praw_submission.title
        self.text = self.praw_submission.selftext
