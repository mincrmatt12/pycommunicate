from pycommunicate.server.bases.views import View
from pycommunicate.server.app.communicate import CommunicateApp
from pycommunicate.server.controller import ControllerFactory
import eventlet


class View1(View):
    def render(self):
        return self.controller.templater.render('view1.html')

    def load(self):
        print 'swapping in 5 seconds'
        eventlet.greenthread.sleep(5)
        self.controller.change_view(1)


class View2(View):
    def render(self):
        return self.controller.templater.render('view2.html')

    def load(self):
        print 'landed'


app = CommunicateApp()
controller = ControllerFactory().add_view(View1).add_view(View2).set_default_view(View1)

app.add_controller("/", controller)

app.set_secret_key("secret!!!")
app.run()
