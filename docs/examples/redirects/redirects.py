from pycommunicate.server.app.communicate import CommunicateApp
from pycommunicate.server.bases.controller import ControllerFactory
from pycommunicate.server.bases.views import View

app = CommunicateApp()


class LandingView1(View):
    def render(self):
        return self.controller.redirect('/land2')


class LandingView2(View):
    def render(self):
        return self.controller.templater.render('land.html')

    def load(self):
        print 'test'
        self.controller.html_wrapper.element_by_selector(
            '#redirect').add_event_listener('click',
                                            lambda: self.controller.redirect(
                                                '/land3'))


class LandingView3(View):
    def render(self):
        return 'Landing view 3'

first_controller = ControllerFactory().add_view(LandingView1).set_default_view(LandingView1)
second_controller = ControllerFactory().add_view(LandingView2).set_default_view(LandingView2)
third_controller = ControllerFactory().add_view(LandingView3).set_default_view(LandingView3)

app.add_controller('/', first_controller)
app.add_controller('/land2', second_controller)
app.add_controller('/land3', third_controller)

app.set_secret_key('secret!')
app.run()
