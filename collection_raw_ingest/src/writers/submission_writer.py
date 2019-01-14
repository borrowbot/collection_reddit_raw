from collection_raw_ingest.src.writers.base_writer import ChunkWriter


class SubmissionWriter(ChunkWriter):
    def __init__(self, logger, sql_parameters, queue_size=16):
        template = {
            "submission_id": "submission_id",
            "creation_datetime": "creation_datetime",
            "retrieval_datetime": "retrieval_datetime",
            "score": "score",
            "num_comments": "num_comments",
            "author_name": "author_name",
            "author_id": "author_id",
            "permalink": "permalink",
            "subreddit_name": "subreddit_name",
            "subreddit_id": "subreddit_id",
            "title": "title",
            "text": "text"
        }
        super().__init__(logger, template, sql_parameters, queue_size)
