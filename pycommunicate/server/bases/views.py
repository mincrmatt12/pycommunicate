class View:
    def __init__(self, controller):
        self.controller = controller
        self.html_wrapper = controller.html_wrapper

    def load(self):