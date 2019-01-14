import MySQLdb as sql
import threading
from datetime import datetime

from baseimage.config import CONFIG

import praw
import collection_raw_ingest.src.psraw as psraw
from collection_raw_ingest.src.writers.submission_writer import SubmissionWriter
from collection_raw_ingest.src.writers.comment_writer import CommentWriter


DEFAULT_START_DATETIME = 0 # 2010-01-01


class Scheduler(object):
    def __init__(self, logger, subreddit):
        self.logger = logger
        self.subreddit = subreddit
        self.reddit = praw.Reddit(**CONFIG['reddit'])
        self.sql_parameters = CONFIG['sql']

        self.job_lock = threading.Lock()
        self.submission_writer = SubmissionWriter(self.logger, CONFIG['sql'])
        self.comment_writer = CommentWriter(self.logger, CONFIG['sql'])

        # self.last_item = self.get_time_bounds()


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
                print(submission.author_fullname)
                print(submission.subreddit)

                self.submission_writer.push(submission)
                counter += 1
            self.submission_writer.flush()

            self.logger.info('ingested {} new submissions'.format(counter))


    # def get_time_bounds(self):
    #     query = 'SELECT MAX(creation_datetime) FROM submissions WHERE subreddit_name={}'.format(self.subreddit)
    #
    #     db = sql.connect(**self.sql_parameters)
    #     cur = db.cursor()
    #     cur.execute(query)
    #     result_set = cursor.fetchall()
    #     print(result_set)
    #     cur.close()
    #     db.close()
