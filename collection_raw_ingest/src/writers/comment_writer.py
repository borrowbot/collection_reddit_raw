from collection_raw_ingest.src.writers.base_writer import ChunkWriter


class CommentWriter(ChunkWriter):
    def __init__(self, logger, sql_parameters, queue_size=16):
        template = {}
        table_name = 'comments'
        super().__init__(logger, template, table_name, sql_parameters, queue_size)
