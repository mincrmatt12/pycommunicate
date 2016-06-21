class ContextAwareFunctionWrapper(object):
    def __init__(self):
        self.create_function = None
        self.functions = {}

    def __get__(self, instance, owner):
        if instance in self.functions:
            return self.functions[instance]
        else:
            self.functions[instance] = self.create_function(instance)
            return self.functions[instance]

