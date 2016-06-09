class StateManager:
    def __init__(self):
        self.is_connected = False
        self.immediate = True
        self.immediate_call_buffer = []

    def request(self, event_name, *args, **kwargs):
        if not self.is_connected:
            raise ValueError('''Attempt to request event from non-existent connection.''')
        pass

    def send(self, event_name, *args, **kwargs):
        pass