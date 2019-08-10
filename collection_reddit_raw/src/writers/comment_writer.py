from lib_learning.collection.batch_writer import BatchWriter


class CommentWriter(BatchWriter):
    def __init__(self, logger, sql_parameters, table_name='submissions', batch_size=16):
        template = {
            'comment_id': 'comment_id',
            'creation_datetime': 'creation_datetime',
            'retrieval_datetime': 'retrieval_datetime',
            'score': 'score',
            'subreddit_name': 'subreddit_name',
            'subreddit_id': 'subreddit_id',
            'text': 'text',
            'link_id': 'link_id',
            'parent_id': 'parent_id',
            'author_name': 'author_name',
            'author_id': 'author_id'
        }
        table_name = 'comments'
        super().__init__(logger, template, table_name, sql_parameters, batch_size)
