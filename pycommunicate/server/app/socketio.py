import flask_socketio
import eventlet


class SocketIOContainer:
    """
    The socketio interface. THIS SHOULD BE THE MAIN ENTRY POINT!!
    """
    def __init__(self, app):
        """

        :type app: pycommunicate.server.app.communicate.CommunicateApp
        """
        self.socketio = flask_socketio.SocketIO(app.flask)
        self.send_queue = eventlet.queue.Queue()
        self.app = app

        self.awaited_responses = {}

        self.create_handlers()

    def on_connect(self, request_id):
        user = self.app.user_tracker.users[self.app.user_tracker.requests[request_id]]

        if user.socket_connected:
            return

        user.socket_connect()

        flask_socketio.join_room(request_id)

    def create_handlers(self):
        @self.socketio.on("setup")
        def connect(request_id):
            self.on_connect(request_id)

        @self.socketio.on("response")
        def response(response_data, tag):
            self.awaited_responses[tag].put(response_data)

    def send(self, event_id, room, args, tag=""):
        thing = (room, event_id, list(args) + [tag] if tag is not "" else [args])
        if tag != "":
            self.awaited_responses[tag] = eventlet.queue.Queue()
        self.send_queue.put(thing)

    def received_response(self, tag):
        return not self.awaited_responses[tag].empty()

    def await_response(self, tag):
        return_value = self.awaited_responses[tag].get()
        del self.awaited_responses[tag]
        return return_value

    def send_daemon(self):
        while True:
            data = self.send_queue.get()
            self.socketio.emit(data[1], data[2], room=data[0])

    def start_handlers(self, pool):
        pool.spawn_n(self.send_daemon)
