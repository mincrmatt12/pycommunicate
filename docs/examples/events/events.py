from pycommunicate.server.app.communicate import CommunicateApp
from pycommunicate.server.bases.controller import ControllerFactory
from pycommunicate.server.bases.views import View


class EventView(View):
    def render(self):
        return self.controller.templater.render("page.html")

    def load(self):
        self.html_wrapper.element_by_selector('button#pushme').add_event_listener('click', self.button_pushed)

    def button_pushed(self):
        self.html_wrapper.element_by_selector('p.change').content.set('I have changed, from the server-side!!')
        self.html_wrapper.element_by_selector('p#time').content.set('0')
        self.add_timer(1, self.timer)

    def timer(self):
        time = int(self.html_wrapper.element_by_selector('p#time').content.get())
        time += 1

        self.html_wrapper.element_by_selector('p#time').content.set('{}'.format(time))

app = CommunicateApp()
controller = ControllerFactory().add_view(EventView).set_default_view(EventView)

app.add_controller('/', controller)

app.set_secret_key("secret!!!")
app.run()