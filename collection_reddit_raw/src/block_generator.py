import MySQLdb as sql
import calendar

from lib_learning.collection.base_generator import WorkBlockGenerator


class RedditRawBlockGenerator(WorkBlockGenerator):
    def __init__(self, sql_params, default_after=1262304000):
        self.sql_params = sql_params
        self.default_after = default_after


    def get_next(self, limit=1):
        after = self.get_newest_submission()
        return {
            'after': after,
            'limit': limit
        }


    def get_newest_submission(self):
        query = 'SELECT MIN(creation_datetime) as min, MAX(creation_datetime) as max FROM submissions'

        db = sql.connect(**self.sql_params)
        cur = db.cursor()
        cur.execute(query)
        db.commit()
        result_set = cur.fetchall()
        cur.close()
        db.close()

        last_result = result_set[0][1]
        if last_result is None:
            return self.default_after

        else:
            return calendar.timegm(last_result.timetuple())
