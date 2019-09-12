import requests
import praw
from datetime import datetime
from dateutil.relativedelta import relativedelta

import collection_reddit_raw.src.psraw as psraw
from lib_borrowbot_core.raw_objects.submission import Submission
from lib_borrowbot_core.raw_objects.comment import Comment
from lib_borrowbot_core.raw_objects.user import User
from lib_learning.collection.base_worker import Worker
from collection_reddit_raw.src.writers.submission_writer import SubmissionWriter
from collection_reddit_raw.src.writers.comment_writer import CommentWriter
from collection_reddit_raw.src.writers.user_lookup_writer import UserLookupWriter


class RedditRawWorker(Worker):
    def __init__(
        self, interface, logger, subreddit, submission_table,
        comment_table, sql_params, reddit_params, cutoff_months=6
    ):
        super().__init__(interface, self.main, logger)

        self.sql_params = sql_params
        self.subreddit = subreddit
        self.reddit_params = reddit_params
        self.cutoff_months = cutoff_months
        self.comment_table = comment_table
        self.submission_table = submission_table

        self.reddit = praw.Reddit(**self.reddit_params)
        self.comment_writer = CommentWriter(self.logger, self.sql_params, self.comment_table, float('inf'))
        self.submission_writer = SubmissionWriter(self.logger, self.sql_params, self.submission_table, float('inf'))
        self.user_lookup_writer = UserLookupWriter(self.logger, self.sql_params, float('inf'))


    def main(self, block):
        assert 'after' in block
        assert 'before' in block
        assert 'limit' in block
        cutoff_time = datetime.utcnow() + relativedelta(months=-self.cutoff_months)

        submissions = []
        iterator = psraw.submission_search(
            self.reddit, q='', subreddit=self.subreddit, limit=block['limit'],
            sort='asc', after=block['after'], before=block['before']
        )
        for submission in iterator:
            self.logger.info("{}: {}".format(
                datetime.fromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                submission.permalink
            ))
            s = Submission(init_object=submission)
            if s.creation_datetime > cutoff_time:
                break
            u = User(user_id=s.author_id, user_name=s.author_name)
            submissions.append(s.submission_id)
            self.submission_writer.push(s)
            if u.user_id is not None and u.user_name is not None:
                self.user_lookup_writer.push(u)
        self.submission_writer.flush()

        if len(submissions) == 0:
            return
        comment_iterator = psraw.comment_search(
            self.reddit, q='', subreddit=self.subreddit, limit=1000000,
            sort='asc', link_id=','.join(submissions)
        )
        for comment in comment_iterator:
            self.logger.info(" | {}".format(
                datetime.fromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S')
            ))
            c = Comment(init_object=comment)
            self.comment_writer.push(c)
        self.comment_writer.flush()
