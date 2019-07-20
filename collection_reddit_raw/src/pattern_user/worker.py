import praw
import collection_reddit_raw.src.psraw as psraw

from lib_borrowbot_core.raw_objects.submission import Submission
from lib_borrowbot_core.raw_objects.comment import Comment
from collection_reddit_raw.src.writers.submission_writer import SubmissionWriter
from collection_reddit_raw.src.writers.comment_writer import CommentWriter


class RedditUserHistoryTask(object):
    def __init__(self, logger, sql_params, reddit_params):
        self.sql_params = sql_params
        self.logger = logger
        self.reddit_params = reddit_params
        self.sql_params = sql_params

        self.reddit = praw.Reddit(**reddit_params)
        # self.comment_writer = CommentWriter(logger, sql_params, float('inf'))
        # self.submission_writer = SubmissionWriter(logger, sql_params, float('inf'))

    def main(self, block):
        submission_iterator = psraw.submission_search(
            self.reddit, author='franklywang', limit=30, sort='asc', after=1483228800
        )
        for submission in submission_iterator:
            s = Submission(submission)
            print(s.creation_datetime)

        comment_iterator = psraw.comment_search(
            self.reddit, author='franklywang', limit=30, sort='asc', after=1483228800
        )
        for comment in comment_iterator:
            c = Comment(comment)
            print(c.creation_datetime)
