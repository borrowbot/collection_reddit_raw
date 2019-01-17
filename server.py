import json
from flask import request

from collection_raw_ingest.src.scheduler import Scheduler
from baseimage.config import CONFIG
from baseimage.flask.flask import get_flask_server
from baseimage.logger import get_default_logger


logger = get_default_logger()
server = get_flask_server()
scheduler = Scheduler(logger, CONFIG['subreddit'])


@server.route("/fill_data", methods=['POST'])
def fill_data():
    limit = request.args.get('limit', type=int, default=1)
    return json.dumps(scheduler.get(limit))


@server.route("/update_data", methods=['POST'])
def update():
    pass


server.run()
