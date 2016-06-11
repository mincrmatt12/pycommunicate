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

Serving up a static page
~~~~~~~~~~~~~~~~~~~~~~~~

First of all, we will need a CommunicateApp instance before we even start writing anything, so lets add that now to
main.py:
.. code-block:: python
   :linenos:
   :emphasize-lines: 3

   from pycommunicate.server.app.communicate import CommunicateApp

   app = CommunicateApp()  # main app instance

