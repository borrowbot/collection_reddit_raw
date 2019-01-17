import MySQLdb as sql
import threading
import calendar
from datetime import datetime

from baseimage.config import CONFIG

import praw
import collection_raw_ingest.src.psraw as psraw
from collection_raw_ingest.src.wrapper_objects.submission import Submission
from collection_raw_ingest.src.wrapper_objects.comment import Comment
from collection_raw_ingest.src.writers.submission_writer import SubmissionWriter
from collection_raw_ingest.src.writers.comment_writer import CommentWriter


# All times in the scheduler logic use seconds from unix epoch
# In the submission wrapper classes and MySQL DB, this is converted to UTC datetime
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
        self.logger.info("initiated submission/comment pipeline")


    def get(self, limit=64):
        with self.job_lock:
            self.logger.info("performing a safe get of {} items".format(limit))
            return self.unsafe_get(self.last_entry, limit)


    def unsafe_get(self, start, limit=64):
        """ A function which ingests raw data into databases. The function pulls, parses, and stores all submissions
            which can be found within the specified range making use of the `psraw` reddit API.

        Args
            start <string>: A interger representing seconds from the unix epoch
        """
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
            print("{}: {}".format(datetime.fromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S'), submission.permalink))
            self.submission_writer.push(Submission(submission))

            comment_iterator = psraw.comment_search(
                self.reddit, q='', subreddit=self.subreddit, limit=100000,
                sort='asc', link_id=submission.id
            )
            for comment in comment_iterator:
                print(" | {}".format(datetime.fromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S')))
                self.comment_writer.push(Comment(comment))

            counter += 1

        self.last_entry = submission.created_utc
        self.submission_writer.flush()

        self.logger.info('ingested {} new submissions'.format(counter))

        return {
            "run_parameters": {"start": start, "limit": limit,},
            "old_bounds": {"start": old_first, "end": old_last},
            "new_bounds": {"start": self.first_entry, "end": self.last_entry},
            "num_new_items": counter
        }


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
            self.logger.info("no historical data found, starting with {} as a bound".format(self.first_entry))

        else:
            self.first_entry = calendar.timegm(self.first_entry.timetuple())
            self.last_entry = calendar.timegm(self.last_entry.timetuple())
            self.logger.info("found existing data with time bounds {}, {}".format(self.first_entry, self.last_entry))
