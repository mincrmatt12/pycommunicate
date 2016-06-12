class CallCTX:
    def __init__(self, **exposed):
        self.__stuff = exposed
        self.__active = True

    def use(self, name):
        if self.__active:
            return self.__stuff[name]

        return None

    def deactivate(self):
        self.__stuff = {}
        self.__active = False
