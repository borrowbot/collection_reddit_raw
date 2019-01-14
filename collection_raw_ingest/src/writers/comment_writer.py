from collection_raw_ingest.src.writers.base_writer import ChunkWriter


class CommentWriter(ChunkWriter):
    def __init__(self, logger, sql_parameters, queue_size=16):
        template = {}
        super().__init__(logger, template, sql_parameters, queue_size)
