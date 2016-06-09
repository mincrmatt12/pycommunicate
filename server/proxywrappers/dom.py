class HTMLWrapper:
    def __init__(self, state_manager):
        self.state_manager = state_manager
        pass


class Element:
    def __init__(self, html_wrapper, identifier):
        self.html_wrapper = html_wrapper
        self.identifier = identifier


class SimpleElementProperty:
    def __init__(self, state_manager, element, inner_name):
        self.state_manager = state_manager
        self.element = element
        self.inner_name = inner_name

    def __get__(self, instance, owner):
        return self.state_manager.request('element.get.property', self.element.identifier, self.inner_name)

    def __set__(self, instance, value):
        self.state_manager.send('element.set.property', self.element.identifier, self.inner_name, value)