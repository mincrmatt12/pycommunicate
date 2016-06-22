ctx = None


class ContextAwareWrapper:
    def __init__(self, get):
        self.get = get

    def __get__(self, instance, owner):
        return self.get(ctx)


class Context:
    def __init__(self, name):
        self.name = name
        self.data = {}

    def active(self):
        global ctx
        ctx = self

    def use(self, name, value=None):
        if value:
            self.data[name] = value
        else:
            return self.data[name]
