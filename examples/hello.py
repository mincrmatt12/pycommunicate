"""
hello.py:

Using the pycommunicate framework to serve a static webpage, as well as show internal id numbers. It also shows off the
session stuff.

Because the returned value does not load the js libs, the socketio connection is not started. This means that
none of the apis will work nor will load ever be called. Again, this is a very simple demo.

WARNING: DO NOT ACTUALLY SHOW THE USER ID TO A USER!!
"""

from pycommunicate.server.bases.views import View
from pycommunicate.server.app.communicate import CommunicateApp
from pycommunicate.server.controller import ControllerFactory


class HelloView(View):
    def render(self):
        if 'count' in self.controller.user.session:
            self.controller.user.session['count'] += 1
        else:
            self.controller.user.session['count'] = 1
        return ("Hello World! My user id is {}, and my request id is {}. The session says you have requested this {}"
                " times").format(
            self.controller.user.id_,
            self.controller.user.request_id,
            self.controller.user.session['count'])


app = CommunicateApp()
controller = ControllerFactory().add_view(HelloView).set_default_view(HelloView)

app.add_controller("/", controller)

app.set_secret_key("secret!!!")
app.run()
