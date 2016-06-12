from werkzeug.utils import redirect

from pycommunicate.proxies.dom.html import HTMLWrapper
from pycommunicate.proxies.socket import SocketInterface


class Controller:
    """
    Real controller instance, created by a ControllerFactory

    These are populated automagically, and should not be created externally
    """
    def __init__(self, factory):
        self.view_index = factory.default_view_index
        self.app = None
        self.route_data = {}
        self.d = {}  # The data object, maybe replace this with some proxy thingy later
        self.user = None
        self.route = factory.route
        self.socket_interface = SocketInterface(self)
        self.html_wrapper = HTMLWrapper(self)
        self.templater = None
        self.before_connect = factory.before_connect
        self.special_return_handler = None

        self.events = {}

        self.views = [view(self) for view in factory.view_types]

    def render_page(self):
        return self.views[self.view_index].render()

    def current_view(self):
        return self.views[self.view_index]

    def change_view(self, new_view_index):
        self.view_index = new_view_index
        self.socket_interface.send('view.swap', self.render_page())
        self.user.socket_connected = False

    def redirect(self, location):
        # noinspection PyBroadException
        try:
            self.socket_interface.send('page.change', location)
        except:
            pass
        self.special_return_handler = lambda: redirect(location)
        return None

    def trigger_connect(self):
        self.current_view().load()

    def teardown(self):
        for event_id in self.events:
            del self.app.socketio.event_dispatchers[event_id]
        for view in self.views:
            view.teardown()

    def dispatch_event(self, event_id):
        self.events[event_id]()

    def handle_event(self, event_id, handler):
        def dispatcher():
            self.dispatch_event(event_id)

        self.events[event_id] = handler
        self.app.socketio.event_dispatchers[event_id] = dispatcher


class ControllerFactory:
    def __init__(self):
        self.view_types = []
        self.default_view_index = -1
        self.route = ""
        self.before_connect = lambda x: None

    def add_view(self, view):
        """
        Adds a view type to the list.
        """
        self.view_types += [view]
        return self

    def set_default_view(self, view):
        self.default_view_index = self.view_types.index(view)
        return self

    def with_before_connect(self, before_connect):
        self.before_connect = before_connect
        return self

    def __call__(self, *args, **kwargs):
        controller = Controller(self)
        return controller
