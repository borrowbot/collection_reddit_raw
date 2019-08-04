import MySQLdb as sql
import calendar

from lib_learning.collection.base_generator import WorkBlockGenerator


class RedditRawBlockGenerator(WorkBlockGenerator):
    def __init__(self, sql_params, submission_table, subreddit_name, left_bound):
        self.sql_params = sql_params
        self.left_bound = left_bound
        self.subreddit_name = subreddit_name
        self.submission_table = submission_table


    def get_next(self, after, before, limit):
        default_after = self.get_newest_submission()

        if limit is None:
            assert after is not None and before is not None
            assert after >= self.left_bound and after <= default_after
            assert before - after < 60 * 60 * 24
            limit = 1000000

        else:
            assert after is None and before is None
            after = default_after
            before = 4102444800 # 2100-01-01

        return {
            'after': after,
            'before': before,
            'limit': limit
        }


    def get_newest_submission(self):
        query = '''
        SELECT MIN(creation_datetime) as min, MAX(creation_datetime) as max
        FROM {}
        WHERE subreddit_name="{}"
        '''.format(self.submission_table, self.subreddit_name)

        db = sql.connect(**self.sql_params)
        cur = db.cursor()
        cur.execute(query)
        db.commit()
        result_set = cur.fetchall()
        cur.close()
        db.close()

        last_result = result_set[0][1]
        if last_result is None:
            return self.left_bound

        else:
            return calendar.timegm(last_result.timetuple())
