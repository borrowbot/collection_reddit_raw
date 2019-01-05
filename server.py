from baseimage.flask.flask import get_flask_server

server = get_flask_server()

@server.route("/")
def hello():
    return "Hello World!"

server.run()
