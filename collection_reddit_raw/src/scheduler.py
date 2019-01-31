from datetime import datetime
import praw

from lib_collection.scheduler import Scheduler

import collection_raw_ingest.src.psraw as psraw
from collection_raw_ingest.src.wrapper_objects.submission import Submission
from collection_raw_ingest.src.wrapper_objects.comment import Comment
from collection_raw_ingest.src.writers.submission_writer import SubmissionWriter
from collection_raw_ingest.src.writers.comment_writer import CommentWriter


class SubRedditScheduler(Scheduler):
    """ A API request scheduler for ingesting reddit submissions and posts from a single subreddit. This scheduler gets
        PRAW submission and comment objects making use of the pushshift.io API and writes them to a MySQL table. Safe
        usage of this class ensures contiguous, complete, and non-dupicate data. See the README.md for more details.
    """
    def initialize_custom_attributes(self, subreddit, reddit_params):
        self.submission_writer = SubmissionWriter(self.logger, self.sql_parameters, batch_size=4)
        self.comment_writer = CommentWriter(self.logger, self.sql_parameters, batch_size=8)
        self.subreddit = subreddit
        self.reddit_params = reddit_params
        self.reddit = praw.Reddit(**self.reddit_params)


    def get_time_bounds_query(self):
        return 'SELECT MIN(creation_datetime) as min, MAX(creation_datetime) as max FROM submissions WHERE subreddit_name="{}"'.format(self.subreddit)


    def unsafe_get(self, start, limit=64):
        self.logger.info("ingesting data from after {} (limit {})".format(
            datetime.fromtimestamp(start).strftime('%Y-%m-%d %H:%M:%S'),
            limit
        ))
        old_first = self.first_entry
        old_last = self.last_entry

        iterator = psraw.submission_search(
            self.reddit, q='', subreddit=self.subreddit,
            limit=limit, sort='asc', after=start
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

        self.last_entry = submission.created_utc
        self.submission_writer.flush()
        self.comment_writer.flush()

        self.logger.info('ingested {} new submissions'.format(counter))

        return {
            "run_parameters": {"start": start, "limit": limit,},
            "old_bounds": {"start": old_first, "end": old_last},
            "new_bounds": {"start": self.first_entry, "end": self.last_entry},
            "num_new_items": counter
        }
