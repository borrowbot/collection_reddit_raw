from sqlalchemy import create_engine
import MySQLdb as sql
import pandas as pd
import calendar

from lib_learning.collection.base_generator import WorkBlockGenerator


def chunk_list(list, chunk_size):
    return (list[i:i+chunk_size] for i in range(0, len(list), chunk_size))


class RedditUserHistoryBlockGenerator(WorkBlockGenerator):
    def __init__(
        self, sql_params, submission_table, comment_table,
        reference_submission_table, reference_comment_table, chunk_size, left_bound
    ):
        self.sql_params = sql_params
        self.submission_table = submission_table
        self.comment_table = comment_table
        self.reference_submission_table = reference_submission_table
        self.reference_comment_table = reference_comment_table
        self.chunk_size = chunk_size
        self.left_interval = left_bound
        self.right_interval = self.get_right_interval()


    def get_known_users(self):
        query = '''
            SELECT *
            FROM (
                SELECT DISTINCT(author_name) FROM {}
                UNION ALL
                SELECT DISTINCT(author_name) FROM {}
            ) joined_table
        '''.format(self.submission_table, self.comment_table)

        db = sql.connect(**self.sql_params)
        cur = db.cursor()
        cur.execute(query)
        db.commit()
        result_set = cur.fetchall()
        cur.close()
        db.close()

        return set([r[0] for r in result_set if r[0] is not None])


    def get_all_users(self):
        query = '''
            SELECT DISTINCT(author_name)
            FROM (
                (SELECT author_name FROM {})
                UNION ALL
                (SELECT author_name FROM {})
            ) alias
        '''.format(self.reference_comment_table, self.reference_submission_table)
        db = sql.connect(**self.sql_params)
        cur = db.cursor()
        cur.execute(query)
        db.commit()
        result_set = cur.fetchall()
        cur.close()
        db.close()

        return set([r[0] for r in result_set if r[0] is not None])


    def get_right_interval(self):
        query = '''
            SELECT
                MAX(creation_datetime) AS max_dt
            FROM
            (
                SELECT creation_datetime FROM {}
                UNION ALL
                SELECT creation_datetime FROM {}
            ) joined_table
        '''.format(self.submission_table, self.comment_table)
        db = sql.connect(**self.sql_params)
        cur = db.cursor()
        cur.execute(query)
        db.commit()
        result_set = cur.fetchall()
        cur.close()
        db.close()

        if result_set[0][0] is None:
            return self.left_interval
        return calendar.timegm(result_set[0][0].timetuple())


    def get_next(self, interval):
        assert interval <= 24 * 60 * 60
        new_right_interval = self.right_interval + interval
        all_users = self.get_all_users()
        known_users = self.get_known_users()

        new_user_work_packets = [{
            'username': ','.join(wp),
            'after': self.left_interval,
            'before': new_right_interval,
        } for wp in chunk_list(list(all_users - known_users), self.chunk_size)]

        old_user_work_packets = [{
            'username': ','.join(wp),
            'after': self.right_interval,
            'before': new_right_interval,
        } for wp in chunk_list(list(known_users), self.chunk_size)]

        self.right_interval = new_right_interval
        return new_user_work_packets + old_user_work_packets
