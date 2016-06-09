from ...util import random_alphanumeric_string


class UserTracker:
    """
    Tracks all user ids and creates new ones
    """
    def __init__(self, app):
        self.user_refs = []
        self.users = []
        self.app = app

    def connect_user(self):
        id_ = random_alphanumeric_string(50)
        while id_ in self.user_refs:
            id_ = random_alphanumeric_string(50)
        self.user_refs.append(id_)
        user = ConnectedUser(id_, self.app)
        self.users.append(user)
        return user

    def disconnect_user(self, user):
        self.users.remove(user)
        self.user_refs.remove(user.id_)


class ConnectedUser:
    def __init__(self, id_, app):
        self.id_ = id_
        self.app = app
        self.active_controller = None
        self.active_controller_type = None

    def open_page(self, page):
        self.active_controller_type = self.app.routed_controllers[page]
        self.active_controller = self.active_controller_type()