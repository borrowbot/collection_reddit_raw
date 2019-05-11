from lib_learning.collection.batch_writer import BatchWriter


class UserLookupWriter(BatchWriter):
    def __init__(self, logger, sql_parameters, batch_size=16):
        template = {
            "user_id": "user_id",
            "user_name": "user_name"
        }
        table_name = "user_lookup"
        super().__init__(logger, template, table_name, sql_parameters, batch_size)
