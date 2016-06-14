from pycommunicate.server.app.communicate import CommunicateApp
from pycommunicate.server.bases.controller import ControllerFactory
from pycommunicate.server.bases.views import View


class EventView(View):
    def render(self):
        return self.controller.templater.render("page.html")

    def load(self):
        self.html_wrapper.element('button#pushme').add_event_listener('click', self.button_pushed)

    def button_pushed(self):
        self.html_wrapper.element('p.change').content = 'I have changed, from the server-side!!'
        self.html_wrapper.element('p#time').content = '0'
        self.add_timer(1, self.timer)

    def timer(self):
        time = int(self.html_wrapper.element('p#time').content)
        time += 1

        self.html_wrapper.element('p#time').content = '{}'.format(time)

app = CommunicateApp()
controller = ControllerFactory().add_view(EventView).set_default_view(EventView)

app.add_controller('/', controller)

app.set_secret_key("secret!!!")
app.run()