
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
   An instance of CommunicateApp. This is the main thing inside pycommunicate based webapps.


Now lets explain them in a bit more detail:

Controller
~~~~~~~~~~

A controller is probably not what you think it is, as this does not follow MVC. Instead, controllers are used
to hold many views, which actually deal with the page. Controller do, however, contain the controller session, which
is one of many sessions in pycommunicate. This one remains across any given request.

Controllers are not created by you, though. They are created by pycommunicate itself, you only define one. For this
you use ControllerFactory.

View
~~~~

Views probably contain the bulk of your code. They are responsible for serving up a page, handling events in a page, and
much more. Because of this, views are subclassed from the base View class.


OK, I promise in the next part we can start actually programming something!