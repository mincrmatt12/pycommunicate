How pycommunicate works
=======================

Before we can start writing code, let's get some terms and stuff out of the way:

controller
   A collection of views that manages one specific route. Can be thought of as a 'page'

view
   One page option for a controller, the bulk of ui code and the render function resides here. Can be
   thought of as a 'sub-page'

request
   A unique request for a controller.

app
   An instance of :py:class:`~pycommunicate.server.app.communicate.CommunicateApp`. This is the main thing inside pycommunicate based webapps.


Now lets explain them in a bit more detail:

Controller
~~~~~~~~~~

A controller is probably not what you think it is, as this does not follow MVC. Instead, controllers are used
to hold many views, which actually deal with the page. :py:class:`~pycommunicate.server.bases.controller.Controller` instances are
what controllers are. Controllers contain the controller session, which is one of many sessions in pycommunicate.
This one remains across any given request.

Controllers are not created by you, though. They are created by :py:class:`~pycommunicate.server.bases.controller.ControllerFactory`
instances. You can subclass both :py:class:`~pycommunicate.server.bases.controller.Controller`
and :py:class:`~pycommunicate.server.bases.controller.ControllerFactory` to create your own custom behaviour, however.

View
~~~~

Views probably contain the bulk of your code. They are responsible for serving up a page, handling events in a page, and
much more. Because of this, views are subclassed from the base :py:class:`~pycommunicate.server.bases.views.View` class.


OK, I promise in the next part we can start actually programming something!