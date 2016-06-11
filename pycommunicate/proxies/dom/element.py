from pycommunicate.proxies.dom.property import SimpleElementProperty, MultiElementProperty
from pycommunicate.util import random_alphanumeric_string


class ElementWrapper:
    def __init__(self, html_wrapper, selector):
        self.dom = html_wrapper
        self.selector = selector
        self.content = SimpleElementProperty('innerText', self)  # TODO: Wrap more elements without set and get
        self.style = MultiElementProperty('style', self)

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

    def append_element_after_self(self, element_type, id):
        self.dom.controller.socket_interface.request('element.add.after', self.selector, element_type.upper(), id)
        return ElementWrapper(self.dom, "{}#{}".format(element_type.lower(), id))

    def append_element_inside_self(self, element_type, id):
        self.dom.controller.socket_interface.request('element.add.inside', self.selector, element_type.upper(), id)
        return ElementWrapper(self.dom, "{}#{}".format(element_type.lower(), id))

    def delete(self):
        self.dom.controller.socket_interface.send('element.remove', self.selector)

