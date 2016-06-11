from pycommunicate.proxies.dom.property import SimpleElementProperty
from pycommunicate.util import random_alphanumeric_string


class ElementWrapper:
    def __init__(self, html_wrapper, selector):
        self.dom = html_wrapper
        self.selector = selector
        self.content = SimpleElementProperty('innerText', self)

    def set_property(self, property_name, value):
        self.dom.controller.socket_interface.send('element.property.set', self.selector, property_name,
                                                  value)

    def get_property(self, property_name):
        return self.dom.controller.socket_interface.request('element.property', self.selector, property_name)

    def add_event_listener(self, event_name, handler):
        event_id = random_alphanumeric_string(75)

        while event_id in self.dom.controller.app.socketio.event_dispatchers:
            event_id = random_alphanumeric_string(75)

        self.dom.controller.handle_event(event_id, handler)
        self.dom.controller.socket_interface.send('element.addevent', self.selector, event_name, event_id)
