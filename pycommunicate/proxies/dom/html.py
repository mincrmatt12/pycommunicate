from pycommunicate.proxies.dom.element import ElementWrapper


class HTMLWrapper:
    def __init__(self, controller):
        self.controller = controller

    def exists(self, selector):
        return self.controller.socket_interface.request('element.exists', selector)

    def element(self, selector):
        if self.exists(selector):
            return ElementWrapper(self, selector)
        else:
            return None