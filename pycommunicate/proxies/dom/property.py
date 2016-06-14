import pycommunicate.proxies.dom.element


class SimpleElementProperty(object):
    # Deprecated since 0.0.8

    def __init__(self, name, element):
        self.name = name
        self.element = element

    def get(self):
        return self.element.dom.controller.socket_interface.request('element.property', self.element.selector,
                                                                    self.name)

    def set(self, value):
        self.element.dom.controller.socket_interface.send('element.property.set', self.element.selector,
                                                          self.name, value)


class DescriptorElementProperty(object):
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        if not isinstance(instance, pycommunicate.proxies.dom.element.ElementWrapper):
            raise AttributeError('''Cannot get element property from other than element''')
        element = instance
        return element.dom.controller.socket_interface.request('element.property', element.selector, self.name)

    def __set__(self, instance, value):
        if not isinstance(instance,  pycommunicate.proxies.dom.element.ElementWrapper):
            raise AttributeError('''Cannot set element property from other than element''')
        element = instance
        element.dom.controller.socket_interface.send('element.property.set', element.selector, self.name, value)


class MultiElementProperty(object):
    def __init__(self, basename, element):
        self.element = element
        self.basename = basename

    def __getitem__(self, item):
        return self.element.dom.controller.socket_interface.request('element.property.complex', self.element.selector,
                                                                    self.basename, item)

    def __setitem__(self, key, value):
        return self.element.dom.controller.socket_interface.send('element.property.complex.set', self.element.selector,
                                                                 self.basename, key, value)
