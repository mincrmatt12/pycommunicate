from pycommunicate.server.bases.views import View
from pycommunicate.server.app.communicate import CommunicateApp
from pycommunicate.server.controller import ControllerFactory


class HelloView(View):
    def render(self):
        return self.controller.templater.render('hello2.html')

    def load(self):
        print "connection established"


app = CommunicateApp()
controller = ControllerFactory().add_view(HelloView).set_default_view(HelloView)

app.add_controller("/", controller)

app.set_secret_key("secret!!!")
app.run()
