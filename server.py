import json
from flask import request

from collection_raw_ingest.src.scheduler import Scheduler
from baseimage.flask.flask import get_flask_server
from baseimage.logger import get_default_logger


logger = get_default_logger()
server = get_flask_server()
scheduler = Scheduler(logger, "borrow")


@server.route("/fill_data", methods=['POST'])
def fill_data():
    limit = request.args.get('limit', type=int, default=1)
    scheduler.get(limit)
    return "Hello World"


server.run()
