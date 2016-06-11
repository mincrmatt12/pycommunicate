from pycommunicate.proxies.socket import SocketInterface


class Controller:
    """
    Real controller instance, created by a ControllerFactory

    These are populated automagically, and should not be created externally
    """
    def __init__(self, factory):
        self.views = [view(self) for view in factory.view_types]
        self.view_index = factory.default_view_index
        self.app = None
        self.route_data = {}
        self.d = {}  # The data object, maybe replace this with some proxy thingy later
        self.user = None
        self.route = factory.route
        self.socket_interface = SocketInterface(self)
        self.templater = None

    def render_page(self):
        return self.views[self.view_index].render()

    def current_view(self):
        return self.views[self.view_index]

    def change_view(self, new_view_index):
        pass

    def trigger_connect(self):
        self.current_view().load()


class ControllerFactory:
    def __init__(self):
        self.view_types = []
        self.default_view_index = -1
        self.route = ""

    def add_view(self, view):
        """
        Adds a view type to the list.
        """
        self.view_types += [view]
        return self

    def set_default_view(self, view):
        self.default_view_index = self.view_types.index(view)
        return self

    def __call__(self, *args, **kwargs):
        controller = Controller(self)
        return controller
