from collection_raw_ingest.src.scheduler import Scheduler
from baseimage.flask.flask import get_flask_server


server = get_flask_server()
scheduler = Scheduler()


@server.route("/fill_data?start=<start>&end=<end>", methods=['POST'])
def fill_data(start, end):
    print("{},{}".format(start, end))
    return "Hello World"


server.run()
