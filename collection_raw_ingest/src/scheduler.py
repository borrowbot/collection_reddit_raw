import threading
from datetime import datetime

from baseimage.config import CONFIG

import praw
import collection_raw_ingest.src.psraw as psraw
from collection_raw_ingest.src.writers.submission_writer import SubmissionWriter
from collection_raw_ingest.src.writers.comment_writer import CommentWriter


class Scheduler(object):
    def __init__(self, logger, subreddit):
        self.logger = logger
        self.subreddit = subreddit
        # self.reddit = praw.Reddit(
        #     client_id='EXmKlisPai3bBA',
        #     client_secret='M-f_hLb4F3XMSDa1tWIHjQyACMs',
        #     password='kj7XRQ%PJ2cb',
        #     user_agent='frank_and_yoon',
        #     username='lee-y'
        # )
        self.reddit = praw.Reddit(**CONFIG['reddit'])

        self.job_lock = threading.Lock()
        self.submission_writer = SubmissionWriter(self.logger, CONFIG['sql'])
        self.comment_writer = CommentWriter(self.logger, CONFIG['sql'])


    def get(self, start, end):
        """ A function which ingests raw data into databases. The function pulls, parses, and stores all submissions
            which can be found within the specified range making use of the `psraw` reddit API.

        Args
            start <string>: Either a datetime as unix epoch or a submission id.
            end <string>: See `start`. The type of this string must match `start`. If a submission id is used,
                you must insure that the ending submission occurs temporally after the start.
        """
        with self.job_lock:
            start, end, date_format = self.check_parse_inputs(start, end)

            if date_format:
                iterator = self.get_datetime_iterator(start, end)
            else:
                iterator = self.get_id_iterator(start, end)

            for submission in iterator:
                self.submission_writer.push(submission)
            self.submission_writer.flush()


    def parse_string(self, string):
        try:
            return int(string)
        except:
            return string


    def check_parse_inputs(self, start, end):
        start, end = self.parse_string(start), self.parse_string(end)
        if isinstance(start, int):
            date_format = True
        else:
            date_format = False

        assert type(start) == type(end)
        if date_format:
            assert start < end

        return start, end, date_format


    def get_datetime_iterator(start, end):
        return psraw.submission_search(
            self.reddit, q='', subreddit=self.subreddit,
            limit=1, sort='desc', after=start, before=end
        )
