class SimpleElementProperty(object):
    def __init__(self, name, element):
        self.name = name
        self.element = element

    def get(self):
        return self.element.dom.controller.socket_interface.request('element.property', self.element.selector,
                                                                    self.name)

    def set(self, value):
        self.element.dom.controller.socket_interface.send('element.property.set', self.element.selector,
                                                          self.name, value)


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


