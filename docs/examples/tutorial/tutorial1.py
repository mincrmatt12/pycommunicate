import eventlet

from pycommunicate.server.bases.views import View
from pycommunicate.server.bases.controller import ControllerFactory
from pycommunicate.server.app.communicate import CommunicateApp

app = CommunicateApp()


class TodoView(View):
    def render(self):
        return self.controller.templater.render("home.html")

controller = ControllerFactory().add_view(TodoView).set_default_view(TodoView)
app.add_controller("/", controller)

app.set_secret_key("secret!")
app.run()

