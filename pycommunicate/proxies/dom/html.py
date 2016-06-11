class HTMLWrapper:
    def __init__(self, controller):
        self.controller = controller

    def element_exists(self, selector):
        return self.controller.socket_interface.request('element.exists', selector)