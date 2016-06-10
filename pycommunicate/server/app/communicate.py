from flask import Flask, session

from pycommunicate.server.app.usertrack import UserTracker
from .socketio import SocketIOContainer
from eventlet.greenpool import GreenPool


class CommunicateApp:
    def __init__(self, web_port=8080, host='localhost', debug=False, maximum_handler_threads=1000):
        self.maximum_handler_threads = maximum_handler_threads
        self.debug = debug
        self.host = host
        self.web_port = web_port

        self.routed_controllers = {}

        self.flask = Flask(__name__)
        self.socketio = SocketIOContainer(self.flask)
        self.user_tracker = UserTracker(self)

        self.green_pool = GreenPool(self.maximum_handler_threads)

    def _dispatch(self, route, **kwargs):
        user = None
        if 'shared_id' in session:
            if session['shared_id'] in self.user_tracker.user_refs:
                user = self.user_tracker.users[session['shared_id']]
        elif user is None:
            user = self.user_tracker.connect_user()
            session['shared_id'] = user.id_

        user.open_page(route, kwargs)
        return user.active_controller.render_page()

    def _create_flask_handler(self, route):
        @self.flask.route(route)
        def handler(**kwargs):
            return self._dispatch(route, **kwargs)

    def add_controller(self, route, controller):
        self.routed_controllers[route] = controller
        self._create_flask_handler(route)

    def run(self):
        self.socketio.socketio.run(self.flask, self.host, self.web_port)
