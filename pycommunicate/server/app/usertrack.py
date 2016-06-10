from ...util import random_alphanumeric_string


class UserTracker:
    """
    Tracks all user ids and creates new ones
    """
    def __init__(self, app):
        self.user_refs = []
        self.users = {}
        self.app = app

    def connect_user(self):
        id_ = random_alphanumeric_string(50)
        while id_ in self.user_refs:
            id_ = random_alphanumeric_string(50)
        self.user_refs.append(id_)
        user = ConnectedUser(id_, self.app)
        self.users[id_] = user

        return user

    def disconnect_user(self, user):
        del self.users[user.id_]
        self.user_refs.remove(user.id_)


class ConnectedUser:
    def __init__(self, id_, app):
        """

        :type app: pycommunicate.server.app.communicate.CommunicateApp
        """
        self.id_ = id_
        self.request_id = ""
        self.app = app
        self.active_controller = None
        self.active_controller_type = None

    def open_page(self, page, kwargs):
        self.request_id = random_alphanumeric_string(60)
        self.active_controller_type = self.app.routed_controllers[page]
        self.active_controller = self.active_controller_type()
        self.active_controller.app = self.app
        self.active_controller.route_data = kwargs
        self.active_controller.user = self

    def socket_connect(self):
        self.app.green_pool.spawn_n(self.active_controller.trigger_connect)
