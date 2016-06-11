Sprinkling in some server-side stuff
====================================

Alright, now that we've got a page working, let's add some functionality.

Before we do that, though, add this class to the main.py file. It contains some multithreading and fileio stuff
to make it easy to add and remove tasks.

.. literalinclude:: todomanager.py
   :language: python
   :linenos:

This should go somewhere after the creation of ``app`` instance

After that, but before the view code, add this to properly initialize it:

.. code-block:: python
   :linenos:

   todo = TodoReader()
   todo.start()

Alright, so now we have a variable called ``todo`` that manages... todos!

Showing the current todos
-------------------------

At the heart of server-side DOM manipulation in pycommunicate is :py:class:`HTMLWrapper`.
For all of the methods it supports, go look at it, but the one we will be using is :py:meth:`element_by_selector`. This method
will return a :py:class:`ElementWrapper` tracked to follow the selector given. This can then be used to modify the DOM.

Add a load() method
~~~~~~~~~~~~~~~~~~~

When a user loads a page with the pycommunicate libraries installed, as soon as ``document.ready()`` occurs client-side, the library
will connect to the server and when the server finishes initializing the connection, the active view's ``load()`` method is called.

Let's create this method and add some code to it after the ``render()`` method:

.. code-block:: python
   :linenos:

   def load(self):
        todo_div = self.html_wrapper.element_by_selector("#todo")

        loading_message = self.html_wrapper.element_by_selector("#loadingBar")
        loading_message.delete()

        for index in todo.todos:
            text = todo.todos[index]
            todo_page_div = todo_div.append_element_inside_self("div", "todo{}".format(index))
            text_p = todo_page_div.append_element_inside_self("p", "todoText{}".format(index))
            text_p.content.set(text)
            button = todo_page_div.append_element_inside_self("button", "todoRemove{}".format(index))
            button.add_event_listener("click", self.make_handler(index))
            button.content.set("Remove")

After doing this, if you are using an IDE, it will complain about self.make_handler not existing, so make that too:

.. code-block:: python
   :linenos:

   def make_handler(self, index):
        def handler():
            todo.remove(index)

            todo_div = self.html_wrapper.element_by_selector("#todo{}".format(index))
            todo_div.delete()
        return handler

Alright, so lets explain what's actually happening there

What's going on in the load() function ?!
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Alright, lets do this bit by bit:

.. code-block:: python
   :linenos:
   :lineno-start: 2

   todo_div = self.html_wrapper.element_by_selector("#todo")

The first part is probably self-explanatory to all python programmers, so let's explain that call. As I said earlier
the :py:meth:`element_by_selector` method returns a :py:class:`ElementWrapper`. In this case, it is tracking the first thing with
an id of ``todo``. In our html file, that points to the ``<div>``. So this call will set todo_div equal to something that represents...
the todo div!

.. code-block:: python
   :linenos:
   :lineno-start: 4

   loading_message = self.html_wrapper.element_by_selector("#loadingBar")
   loading_message.delete()

The first line does similar things to the example above, so lets explain the second line. It calls ``loading_message``'s :py:meth:`delete` method,
which deletes the element. This effectively clears the "Loading..." message from the page.