"""
hello.py:

Using the pycommunicate framework to serve a static webpage, as well as show internal id numbers.

WARNING: DO NOT ACTUALLY SHOW THESE TO A USER!!
"""

from pycommunicate.server.bases.views import View
from pycommunicate.server.app.communicate import CommunicateApp
from pycommunicate.server.controller import ControllerFactory


class HelloView(View):
    def render(self):
        return "Hello World! My user id is {}, and my request id is {}".format(self.controller.user.id_,
                                                                               self.controller.user.request_id)

app = CommunicateApp()
controller = ControllerFactory().add_view(HelloView).set_default_view(HelloView)

app.add_controller("/", controller)

app.set_secret_key("secret!!!")
app.run()
