import json

from collection_raw_ingest.src.scheduler import Scheduler
from baseimage.flask.flask import get_flask_server
from baseimage.logger import get_default_logger


logger = get_default_logger()
server = get_flask_server()
scheduler = Scheduler(logger, "bborrow")


@server.route("/fill_data?start=<start>&end=<end>", methods=['POST'])
def fill_data(start, end):
    print("{},{}".format(start, end))
    return "Hello World"


server.run()
