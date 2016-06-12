Creating your first pycommunicate app
=====================================

Alright, now we can actually start.

The tutorial project will be quite simple:

* will serve up a todo-file
* will allow adding and removing of entries to it

As you can see, this will be very simple, but using other libraries might require lots of ajax processing.
In pycommunicate, none of this is needed!


Let's get started by making the simplest example: serving up a static page.

Setting up our app
------------------
Let's start by making an empty directory called tutorial somewhere on your system. Inside this directory should
be one file and one folder: main.py and templates. We'll get back to templates in a second, but for now let's make
main.py.

Making our page
---------------
First of all, let's create a simple page for our app in html. Some of it might not make sense right now, but just roll
with it. For now just put this into templates/home.html:

.. literalinclude:: /examples/tutorial/templates/home.html
   :language: html
   :linenos:

Serving up the page statically
------------------------------

First of all, we will need a :py:class:`CommunicateApp` instance before we even start writing anything, so lets add that now to
main.py, and while we're at it, lets import everything we'll need:

.. code-block:: python
   :linenos:
   :emphasize-lines: 6

   import eventlet
   from pycommunicate.server.bases.views import View
   from pycommunicate.server.bases.controller import ControllerFactory
   from pycommunicate.server.app.communicate import CommunicateApp

   app = CommunicateApp()  # main app instance

Now, lets create a view called TodoView, and have it display the content inside home.html.

.. code-block:: python
   :linenos:
   :emphasize-lines: 3

   class TodoView(View):
       def render(self):
           return self.controller.templater.render("home.html")

Alright, let's break this down:

.. code-block:: python

   class TodoView(View):

This defines our view, as all views are subclasses of View, from pycommunicate.server.bases.views

Next, we have the render() method. This is called to get the base page to serve when requested. It is the only
thing you actually have to override. Views have references to their parent controllers, which have Templaters. A
:py:class:`Templater` will render a template, the default location is templates/, but this can be changed. See :py:class:`pycommunicate.server.app.communicate.CommunicateApp` for how to change it.

.. note::
   The templater, and all of pycommunicate use jinja2, a templating engine. For more info on what we provide in jinja2, and
   how to use the templater, go look at its page.

Anyways, now that we have a view, we should create a controller:

.. code-block:: python
   :linenos:

   controller = ControllerFactory().add_view(TodoView).set_default_view(TodoView)
   app.add_controller('/', controller)

This one is pretty simple, we create a :py:class:`ControllerFactory` and call its methods (which are chainable) to add
the TodoView view, and set it as the default (initial) one.

We're almost done, now, and all we have to add is the secret key and the call to run.

.. danger::
   Remember, the secret key must be kept secret. For a truly random secret key, use os.urandom()

.. code-block:: python
   :linenos:

   app.set_secret_key('secret!')
   app.run()

And that's it! You should be able to simply run it and see a static, lifeless page. On the next page, we'll get to adding
some event handlers. Here's the full source right now for copying:

.. literalinclude:: tutorial1.py
   :language: python
   :linenos:
