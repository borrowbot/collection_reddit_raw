import pandas as pd
import MySQLdb as sql
from sqlalchemy import create_engine
import threading


class ChunkWriter(object):
    """ Template is a dictionary which maps an attribute name to a column in the target SQL DB.
    """
    def __init__(self, logger, template, table_name, sql_parameters, batch_size=16):
        self.template = template
        self.table_name = table_name
        self.sql_parameters = sql_parameters
        self.batch_size = batch_size

        self.push_lock = threading.Lock()

        self.work_queue = None
        self.num_items = None
        self.reset_work_queue()


    def push(self, item):
        with self.push_lock:
            new_entry = {self.template[k]: getattr(item, k) for k in self.template}
            self.work_queue = self.work_queue.append(new_entry, ignore_index=True)
            self.num_items += 1

            if self.num_items >= self.batch_size:
                self.unsafe_flush()


    def flush(self):
        with self.push_lock:
            self.unsafe_flush()


    def reset_work_queue(self):
        self.work_queue = pd.DataFrame(columns=self.template.values())
        self.num_items = 0


    def unsafe_flush(self):
        self.clear_existing_entries()
        self.write_new_entries()


    def clear_existing_entries(self):
        pass


    def write_new_entries(self):
        engine = create_engine("mysql://{}:{}@{}/{}?charset=utf8mb4".format(
            self.sql_parameters['user'],
            self.sql_parameters['passwd'],
            self.sql_parameters['host'],
            self.sql_parameters['db'],
        ), convert_unicode=True, encoding='utf-8')
        con = engine.connect()
        self.work_queue.to_sql(self.table_name, con=con, if_exists='append', index=False)
        print(self.work_queue)
        self.reset_work_queue()
