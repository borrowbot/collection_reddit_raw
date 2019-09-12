import os
import json
from flask import request
import requests
import yaml

from baseimage.config import CONFIG
from baseimage.flask import get_flask_server
from baseimage.logger.logger import get_default_logger

from collection_reddit_raw.src.pattern_user.worker import RedditUserHistoryWorker
from collection_reddit_raw.src.pattern_user.block_generator import RedditUserHistoryBlockGenerator

from lib_learning.collection.scheduler import Scheduler
from lib_learning.collection.interfaces.local_interface import LocalInterface


# interface
interface = LocalInterface()

# workers
reddit_key_path = os.path.join(
    CONFIG['base_path'], 'collection_reddit_raw', 'resources',
    'reddit_keys', 'borrowbot1.reddit.yml'
)
with open(reddit_key_path, 'r') as f:
    reddit_key = yaml.load(f)
worker_logger = get_default_logger('worker')
worker = RedditUserHistoryWorker(
    interface, worker_logger, CONFIG['submission_table'],
    CONFIG['comment_table'], CONFIG['sql'], reddit_key
)
worker.start()

# schedulers
scheduler_logger = get_default_logger('scheduler')
block_generator = RedditUserHistoryBlockGenerator(
    CONFIG['sql'], CONFIG['submission_table'], CONFIG['comment_table'],
    CONFIG['reference_submission_table'], CONFIG['reference_comment_table'], 512, CONFIG['left_bound']
)
scheduler = Scheduler(
    'collection_reddit_raw', interface, block_generator, scheduler_logger,
    task_timeout=float('inf'), confirm_interval=60
)

# server
server = get_flask_server()

@server.route('/push', methods=["POST"])
def push():
    interval = request.args.get('interval', type=int, default=None)
    return json.dumps(scheduler.push_next_block(interval=interval))

@server.route('/get_queue')
def get_queue():
    return json.dumps(scheduler.pending_work)
