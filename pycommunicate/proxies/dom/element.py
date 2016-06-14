from pycommunicate.proxies.dom.property import SimpleElementProperty, MultiElementProperty, DescriptorElementProperty
from pycommunicate.util import random_alphanumeric_string


class ElementWrapper(object):
    content = DescriptorElementProperty("innerText")
    value = DescriptorElementProperty("value")
    id = DescriptorElementProperty("id")

    def __init__(self, html_wrapper, selector):
        self.dom = html_wrapper
        self.selector = self.dom.controller.socket_interface.request('element.selector', selector)
        self.style = MultiElementProperty('style', self)

    def prop(self, name, value=None):
        if value is None:
            return self.get_property(name)
        else:
            self.set_property(name, value)
            return self

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

    def add_child(self, kind):
        new_selector = self.dom.controller.socket_interface.request('element.add.inside', self.selector, kind)
        return ElementWrapper(self.dom, new_selector)

    def add_after(self, kind):
        new_selector = self.dom.controller.socket_interface.request('element.add.after', self.selector, kind)
        return ElementWrapper(self.dom, new_selector)

    def add_before(self, kind):
        new_selector = self.dom.controller.socket_interface.request('element.add.before', self.selector, kind)
        return ElementWrapper(self.dom, new_selector)

    def delete(self):
        self.dom.controller.socket_interface.send('element.remove', self.selector)

