import eventlet


class View:

    def __init__(self, controller):
        self.controller = controller
        self.html_wrapper = controller.html_wrapper
        self.timers = []

    def add_timer(self, time, function):
        def timer():
            while True:
                eventlet.greenthread.sleep(time)
                function()

        green_thread = eventlet.greenthread.spawn(timer)
        self.timers.append(green_thread)
        return self.timers.index(green_thread)

    def cancel_timer(self, timer):
        self.timers[timer].kill()

    def teardown(self):
        print inspect.stack()
        for timer in self.timers:
            timer.kill()

    def load(self):
        pass

    def render(self):
        pass