from flask import Flask, session, abort, redirect

from pycommunicate.proxies.context import CallCTX
from pycommunicate.server.app.usertrack import UserTracker
from .socketio import SocketIOContainer
from eventlet.greenpool import GreenPool


class CommunicateApp:
    def __init__(self, web_port=8080, host='localhost', debug=False, maximum_handler_threads=10000,
                 template_directory="templates"):
        self.template_directory = template_directory
        self.maximum_handler_threads = maximum_handler_threads
        self.debug = debug
        self.host = host
        self.web_port = web_port

        self.routed_controllers = {}

        self.flask = Flask(__name__)

        self.socketio = SocketIOContainer(self)
        self.user_tracker = UserTracker(self)
        self.flask.secret_key = "secret!"  # Prevents server from crashing without calling set_secret_key

        self.green_pool = GreenPool(self.maximum_handler_threads)

        @self.flask.route('/__pycommunicate/pycommunicate.js')
        def js_lib():
            return self._do_js_lib()

    def set_secret_key(self, key):
        self.flask.secret_key = key

    def _dispatch(self, route, **kwargs):
        user = None

        if 'shared_id' in session:
            if session['shared_id'] in self.user_tracker.user_refs:
                user = self.user_tracker.users[session['shared_id']]
        if user is None:
            user = self.user_tracker.connect_user()
            session['shared_id'] = user.id_

        user.open_page(route, kwargs)

        ctx = CallCTX(abort=abort)
        user.active_controller.before_connect(ctx)
        ctx.deactivate()

        possible = user.active_controller.render_page()

        if user.active_controller.special_return_handler is not None:
            return user.active_controller.special_return_handler()

        return possible

    def _do_js_lib(self):
        user = None

        if 'shared_id' in session:
            if session['shared_id'] in self.user_tracker.user_refs:
                user = self.user_tracker.users[session['shared_id']]
        if user is None:
            user = self.user_tracker.connect_user()
            session['shared_id'] = user.id_

        return user.active_controller.templater.render('__pycommunicate_js/pycommunicate.js',
                                                       request_id=user.request_id)

    def _create_flask_handler(self, route):
        def handler(**kwargs):
            return self._dispatch(route, **kwargs)
        name = 'handles' + str(len(self.routed_controllers))
        self.flask.add_url_rule(route, name, handler)

    def add_controller(self, route, controller):
        if route.startswith("/__pycommunicate"):
            raise ValueError(
                '''Routes cannot start with /__pycommunicate, as this is reserved for pycommunicate itself''')
        self._add_controller(route, controller)

    def _add_controller(self, route, controller):
        controller.route = route
        self.routed_controllers[route] = controller
        self._create_flask_handler(route)

    def add_error_handler(self, code, controller):
        @self.flask.errorhandler(code)
        def handler(a):
            return redirect("/__pycommunicate/error/{}".format(code))

        self._add_controller("/__pycommunicate/error/{}".format(code), controller)

    def run(self):
        self.socketio.start_handlers(self.green_pool)
        self.socketio.socketio.run(self.flask, self.host, self.web_port)
