import socketio
from flask import Flask


class CommunicateApp:
    def __init__(self, web_port=8080, redis_port=8055, host='localhost', debug=False):
        self.debug = debug
        self.host = host
        self.redis_port = redis_port
        self.web_port = web_port

        self.flask = Flask(__name__)
        self.socketio = socketio.SocketIOContainer(self.flask)