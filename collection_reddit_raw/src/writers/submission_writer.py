from lib_learning.collection.batch_writer import BatchWriter


class SubmissionWriter(BatchWriter):
    def __init__(self, logger, sql_parameters, table_name='comments', batch_size=16):
        template = {
            "submission_id": "submission_id",
            "creation_datetime": "creation_datetime",
            "retrieval_datetime": "retrieval_datetime",
            "score": "score",
            "num_comments": "num_comments",
            "author_name": "author_name",
            "author_id": "author_id",
            "url": "url",
            "upvote_ratio": "upvote_ratio",
            "permalink": "permalink",
            "subreddit_name": "subreddit_name",
            "subreddit_id": "subreddit_id",
            "title": "title",
            "text": "text"
        }
        super().__init__(logger, template, table_name, sql_parameters, batch_size)
