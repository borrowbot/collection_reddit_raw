import json
from flask import request

from collection_raw_ingest.src.scheduler import SubRedditScheduler
from baseimage.config import CONFIG
from baseimage.flask.flask import get_flask_server
from baseimage.logger import get_default_logger


logger = get_default_logger()
server = get_flask_server()
scheduler = SubRedditScheduler(
    logger=logger,
    table_name=None,
    sql_params=CONFIG['sql'],
    timebound_name=None,
    subreddit=CONFIG['subreddit'],
    reddit_params=CONFIG['reddit']
)


@server.route("/fill_data", methods=['POST'])
def fill_data():
    limit = request.args.get('limit', type=int, default=1)
    return json.dumps(scheduler.get(limit))


@server.route("/update_data", methods=['POST'])
def update():
    start = request.args.get('start', type=int)
    limit = request.args.get('limit', type=int, default=1)
    return json.dumps(scheduler.update(start, limit))


server.run(port=CONFIG['port'])
