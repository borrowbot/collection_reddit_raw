import MySQLdb as sql
import threading


class ChunkWriter(object):
    def __init__(self, logger, template, table_name, sql_parameters, queue_size=16):
        self.template = template
        self.table_name = table_name
        self.sql_parameters = sql_parameters
        self.queue_size = queue_size

        self.push_lock = threading.Lock()
        self.work_queue = []
        self.num_items = 0


    def push(self, item):
        with self.push_lock:
            self.work_queue.append(item)
            self.num_items += 1

            if self.num_items >= self.queue_size:
                self.unsafe_flush()


    def flush(self):
        with self.push_lock:
            self.unsafe_flush()


    def unsafe_flush(self):
        self.write_sql()
        self.work_queue = []
        self.num_items = 0


    def write_sql(self):
        # query = 'INSERT INTO {} {} VALUES {};'.format(
        #     self.table_name,
        #     COLUMNS,
        #     VALUES
        # )
        print()
        # db = sql.connect(**self.sql_parameters)
        # cur = db.cursor()
        # cur.execute(query)
        # cur.close()
        # db.close()
