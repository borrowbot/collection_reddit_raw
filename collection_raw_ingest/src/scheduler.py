import MySQLdb as sql
import threading
from datetime import datetime

from baseimage.config import CONFIG

import praw
import collection_raw_ingest.src.psraw as psraw
from collection_raw_ingest.src.wrapper_objects.submission import Submission
from collection_raw_ingest.src.writers.submission_writer import SubmissionWriter
from collection_raw_ingest.src.writers.comment_writer import CommentWriter


DEFAULT_START_DATETIME = 1262304000 # 2010-01-01


class Scheduler(object):
    def __init__(self, logger, subreddit):
        self.logger = logger
        self.subreddit = subreddit
        self.reddit = praw.Reddit(**CONFIG['reddit'])
        self.sql_parameters = CONFIG['sql']

        self.job_lock = threading.Lock()
        self.submission_writer = SubmissionWriter(self.logger, CONFIG['sql'])
        self.comment_writer = CommentWriter(self.logger, CONFIG['sql'])

        self.first_entry = None
        self.last_entry = None
        self.get_time_bounds()
        self.logger.info("found existing data with time bounds {}, {}".format(self.first_entry, self.last_entry))
        self.logger.info("initiated submission/comment pipeline")


    def get(self, start, limit=64):
        """ A function which ingests raw data into databases. The function pulls, parses, and stores all submissions
            which can be found within the specified range making use of the `psraw` reddit API.

        Args
            start <string>: A interger representing seconds from the unix epoch
        """
        with self.job_lock:
            self.logger.info("ingesting data from after {} (limit {})".format(
                datetime.fromtimestamp(start).strftime('%Y-%m-%d %H:%M:%S'),
                limit
            ))

            iterator = psraw.submission_search(
                self.reddit, q='', subreddit=self.subreddit,
                limit=limit, sort='desc', after=start
            )

            counter = 0
            for submission in iterator:
                print("{}: {}".format(datetime.fromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S'), submission.id))
                submission = Submission(submission)
                self.submission_writer.push(submission)
                counter += 1
            self.submission_writer.flush()

            self.logger.info('ingested {} new submissions'.format(counter))


    def get_time_bounds(self):
        query = 'SELECT MIN(creation_datetime) as min, MAX(creation_datetime) as max FROM submissions WHERE subreddit_name="{}"'.format(self.subreddit)

        db = sql.connect(**self.sql_parameters)
        cur = db.cursor()
        cur.execute(query)
        result_set = cur.fetchall()
        cur.close()
        db.close()

        self.first_entry = result_set[0][0]
        self.last_entry = result_set[0][1]

        if self.last_entry is None:
            self.first_entry = DEFAULT_START_DATETIME
            self.last_entry = DEFAULT_START_DATETIME
