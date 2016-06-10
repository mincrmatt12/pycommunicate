import flask_socketio
import eventlet


class SocketIOContainer:
    """
    The socketio interface. THIS SHOULD BE THE MAIN ENTRY POINT!!

     :param flask_app An instance of FlaskContainer


    """
    def __init__(self, flask_app):
        self.socketio = flask_socketio.SocketIO(flask_app)
        self.send_queue = eventlet.queue.Queue()

    def connect_handler(self):
        pass

    def send_daemon(self):
        while True:
            data = self.send_queue.get()
            
            self.socketio.emit(data[1][0], data[1][1], room=data[0][0], namespace=data[0][1])

    def start_handlers(self, pool):
        pool.spawn_n(self.send_daemon)
