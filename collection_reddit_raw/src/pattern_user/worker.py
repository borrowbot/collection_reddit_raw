import praw
import collection_reddit_raw.src.psraw as psraw
import prawcore

from lib_borrowbot_core.raw_objects.submission import Submission
from lib_borrowbot_core.raw_objects.comment import Comment
from lib_learning.collection.base_worker import Worker
from collection_reddit_raw.src.writers.submission_writer import SubmissionWriter
from collection_reddit_raw.src.writers.comment_writer import CommentWriter


class RedditUserHistoryWorker(Worker):
    def __init__(self, interface, logger, submission_table, comment_table, sql_params, reddit_params):
        super().__init__(interface, self.main, logger)

        self.sql_params = sql_params
        self.reddit_params = reddit_params
        self.submission_table = submission_table
        self.comment_table = comment_table

        self.reddit = praw.Reddit(**self.reddit_params)
        self.comment_writer = CommentWriter(self.logger, self.sql_params, self.comment_table, 64)
        self.submission_writer = SubmissionWriter(self.logger, self.sql_params, self.submission_table, 64)


    def main(self, block):
        assert 'username' in block
        assert 'after' in block
        assert 'before' in block

        submission_iterator = psraw.submission_search(
            self.reddit, author=block['username'], limit=100000, sort='asc', after=block['after'], before=block['before']
        )
        for submission in submission_iterator:
            # Try block needed to exclude errors submissions from private subreddits
            try:
                s = Submission(submission)
            except (prawcore.exceptions.NotFound, prawcore.exceptions.Forbidden):
                self.logger.warning("parsing submission {} failed due to 403 or 404".format(submission.id))
                continue
            self.submission_writer.push(s)

        comment_iterator = psraw.comment_search(
            self.reddit, author=block['username'], limit=100000, sort='asc', after=block['after'], before=block['before']
        )
        for comment in comment_iterator:
            # Try block needed to exclude errors comments from private subreddits
            try:
                c = Comment(comment)
            except (prawcore.exceptions.NotFound, prawcore.exceptions.Forbidden):
                self.logger.warning("parsing comment {} failed due to 403 or 404".format(comment.id))
                continue
            self.comment_writer.push(c)

        self.submission_writer.flush()
        self.comment_writer.flush()
