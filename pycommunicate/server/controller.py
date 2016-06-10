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

    def render_page(self):
        return self.views[self.view_index].render()


class ControllerFactory:
    def __init__(self):
        self.view_types = []
        self.default_view_index = -1

    def add_view(self, view):
        """
        Adds a view type to the list.
        """
        self.view_types += [view]

    def set_default_view(self, view):
        self.default_view_index = self.view_types.index(view)

    def __call__(self, *args, **kwargs):
        controller = Controller(self)
        return controller
