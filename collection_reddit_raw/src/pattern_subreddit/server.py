import json
from flask import request
import requests

from baseimage.config import CONFIG
from baseimage.flask import get_flask_server
from baseimage.logger.logger import get_default_logger

from collection_reddit_raw.src.pattern_subreddit.worker import RedditRawWorker
from collection_reddit_raw.src.pattern_subreddit.block_generator import RedditRawBlockGenerator

from lib_learning.collection.workers.base_worker import Worker
from lib_learning.collection.scheduler import Scheduler
from lib_learning.collection.interfaces.local_interface import LocalInterface


# interface
interface = LocalInterface()

# workers
worker_logger = get_default_logger('worker')
worker = RedditRawWorker(
    interface, worker_logger, CONFIG['subreddit'], CONFIG['submission_table'], CONFIG['comment_table'],
    CONFIG['sql'], CONFIG['reddit']
)
worker.start()

# schedulers
scheduler_logger = get_default_logger('scheduler')
block_generator = RedditRawBlockGenerator(
    CONFIG['sql'], CONFIG['submission_table'],
    CONFIG['subreddit'], CONFIG['left_bound']
)
scheduler = Scheduler(
    'collection_reddit_raw', interface, block_generator, scheduler_logger,
    task_timeout=float('inf'), confirm_interval=10
)

# server
server = get_flask_server()

@server.route('/push', methods=["POST"])
def push():
    before = request.args.get('before', type=int, default=None)
    after = request.args.get('after', type=int, default=None)
    limit = request.args.get('limit', type=int, default=None)
    return json.dumps(scheduler.push_next_block(after=after, before=before, limit=limit))

@server.route('/get_queue')
def get_queue():
    return json.dumps(scheduler.pending_work)
