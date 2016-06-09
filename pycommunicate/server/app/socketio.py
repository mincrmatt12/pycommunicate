import flask_socketio
import greenlet


class SocketIOContainer:
    """
    The socketio interface. THIS SHOULD BE THE MAIN ENTRY POINT!!

     :param flask_app An instance of FlaskContainer.
    """
    def __init__(self, flask_app):
        self.socketio = flask_socketio.SocketIO(flask_app)

    def connect_handler(self):
        pass
