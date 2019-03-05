import json
import threading
from flask import request

from baseimage.config import CONFIG
from baseimage.flask import get_flask_server
from baseimage.logger.logger import get_default_logger

from collection_reddit_raw.src.worker import RedditRawTask
from collection_reddit_raw.src.block_generator import RedditRawBlockGenerator
from collection_reddit_raw.src.revert import RedditRawRevert

from lib_learning.collection.workers.base_worker import Worker
from lib_learning.collection.scheduler import Scheduler
from lib_learning.collection.interfaces.local_interface import LocalInterface


# interface
interface = LocalInterface()

# workers
worker_logger = get_default_logger('worker')
task_obj = RedditRawTask(worker_logger, CONFIG['subreddit'], CONFIG['sql'], CONFIG['reddit'])
worker_thread = threading.Thread(target=Worker, args=(interface, task_obj.main, worker_logger))
worker_thread.setDaemon(True)
worker_thread.start()

# schedulers
scheduler_logger = get_default_logger('scheduler')
block_generator = RedditRawBlockGenerator(CONFIG['sql'])
revert_obj = RedditRawRevert(CONFIG['sql'])
scheduler = Scheduler(
    'collection_reddit_raw', interface, block_generator, scheduler_logger, blocking=True,
    revert_fn=revert_obj.revert_fn, task_timeout=600, confirm_interval=10
)

# service server
# TODO: endpoints here should be standardized and moved into lib_learning.collection
server = get_flask_server()


@server.route('/push', methods=["POST"])
def push():
    limit = request.args.get('limit', type=int, default=1)
    return json.dumps(scheduler.push_next_block(limit=limit))


@server.route('/get_queue')
def get_queue():
    return json.dumps(scheduler.pending_work)


if __name__ == "__main__":
    server.run(port=CONFIG['port'])
