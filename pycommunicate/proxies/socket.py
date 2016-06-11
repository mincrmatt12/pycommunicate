from ..util import random_alphanumeric_string


class SocketInterface:
    def __init__(self, controller):
        self.controller = controller

    def request(self, event_id, *args):
        tag = random_alphanumeric_string(75)

        while tag in self.controller.app.socketio.awaited_responses:
            tag = random_alphanumeric_string(75)

        self.controller.app.socketio.send(event_id, self.controller.user.request_id, args, tag=tag)

        return self.controller.app.socketio.await_response(tag)

    def send(self, event_id, *args):
        self.controller.app.socketio.send(event_id, self.controller.user.request_id, args)