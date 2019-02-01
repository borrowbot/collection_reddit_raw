from datetime import datetime
import requests
import praw

import collection_reddit_raw.src.psraw as psraw
from collection_reddit_raw.src.wrapper_objects.submission import Submission
from collection_reddit_raw.src.wrapper_objects.comment import Comment
from collection_reddit_raw.src.writers.submission_writer import SubmissionWriter
from collection_reddit_raw.src.writers.comment_writer import CommentWriter


class RedditRawTask(object):
    def __init__(self, logger, subreddit, sql_params, reddit_params):
        self.sql_params = sql_params
        self.subreddit = subreddit
        self.logger = logger
        self.reddit_params = reddit_params
        self.sql_params = sql_params

        self.reddit = praw.Reddit(**self.reddit_params)
        self.comment_writer = CommentWriter(logger, sql_params, float('inf'))
        self.submission_writer = SubmissionWriter(logger, sql_params, float('inf'))


    def main(self, block):
        assert 'limit' in block
        assert 'after' in block

        iterator = psraw.submission_search(
            self.reddit, q='', subreddit=self.subreddit,
            limit=block['limit'], sort='asc', after=block['after']
        )

        counter = 0
        for submission in iterator:
            self.logger.info("{}: {}".format(
                datetime.fromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                submission.permalink
            ))
            self.submission_writer.push(Submission(submission))

            comment_iterator = psraw.comment_search(
                self.reddit, q='', subreddit=self.subreddit, limit=100000,
                sort='asc', link_id=submission.id
            )

            for comment in comment_iterator:
                self.logger.info(" | {}".format(
                    datetime.fromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S')
                ))
                self.comment_writer.push(Comment(comment))

            counter += 1

        self.submission_writer.flush()
        self.comment_writer.flush()
