from pycommunicate.proxies.dom.element import ElementWrapper


class HTMLWrapper:
    def __init__(self, controller):
        self.controller = controller

    def element_exists(self, selector):
        return self.controller.socket_interface.request('element.exists', selector)

    def element_by_selector(self, selector):
        if self.element_exists(selector):
            return ElementWrapper(self, selector)
        else:
            return None