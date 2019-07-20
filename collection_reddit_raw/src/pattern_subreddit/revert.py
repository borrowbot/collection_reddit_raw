from datetime import datetime
import MySQLdb as sql


class RedditRawRevert(object):
    def __init__(self, sql_params):
        self.sql_params = sql_params


    def revert_fn(self, block):
        removal_cutoff = datetime.utcfromtimestamp(int(block['_retrieval_datetime']))
        sub_query = 'DELETE FROM submissions WHERE retrieval_datetime>="{}"'.format(removal_cutoff)
        com_query = 'DELETE FROM comments WHERE retrieval_datetime>="{}"'.format(removal_cutoff)

        db = sql.connect(**self.sql_params)
        cur = db.cursor()
        cur.execute(sub_query)
        cur.execute(com_query)
        db.commit()
        cur.close()
        db.close()
