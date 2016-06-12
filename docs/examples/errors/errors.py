from pycommunicate.server.app.communicate import CommunicateApp
from pycommunicate.server.bases.controller import ControllerFactory
from pycommunicate.server.bases.views import View

app = CommunicateApp()


class ErrorView(View):
    def render(self):
        return self.controller.templater.render('error.html')


class NormalView(View):
    def render(self):
        return '???'


def aborter(ctx):
    ctx.use("abort")(401)

error_controller = ControllerFactory().add_view(ErrorView).set_default_view(ErrorView)
controller = ControllerFactory().add_view(NormalView).set_default_view(NormalView).with_before_connect(aborter)

app.add_controller("/", controller)
app.add_error_handler(401, error_controller)

app.set_secret_key("secret!!!")
app.run()
