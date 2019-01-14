import threading


class ChunkWriter(object):
    def __init__(self, logger, template, sql_parameters, queue_size=16):
        self.template = template
        self.sql_parameters = sql_parameters
        self.push_lock = threading.Lock()
        self.queue_size = queue_size
        self.work_queue = []
        self.num_items = 0


    def push(self, item):
        with self.push_lock:
            self.work_queue.push(item)
            self.num_items += 1

            if self.num_items >= self.queue_size:
                self.unsafe_flush()


    def flush():
        with self.push_lock:
            self.unsafe_flush()


    def unsafe_flush():
        self.write_sql()
        self.work_queue = []
        self.num_items = 0


    def write_sql(self):
        print(self.work_queue)
