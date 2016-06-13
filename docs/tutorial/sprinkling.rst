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

Showing the current todos and removing them
-------------------------------------------

At the heart of server-side DOM manipulation in pycommunicate is :py:class:`~pycommunicate.proxies.dom.html.HTMLWrapper`.
For all of the methods it supports, go look at it, but the one we will be using is :py:meth:`~pycommunicate.proxies.dom.html.HTMLWrapper.element_by_selector`.
This method will return a :py:class:`~pycommunicate.proxies.dom.element.ElementWrapper` tracked to follow the selector
given. This can then be used to modify the DOM.

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

Alright, let's do this bit by bit:

.. code-block:: python
   :linenos:
   :lineno-start: 2

   todo_div = self.html_wrapper.element_by_selector("#todo")

The first part is probably self-explanatory to all python programmers, so let's explain that call. As I said earlier
the :py:meth:`~pycommunicate.proxies.dom.html.HTMLWrapper.element_by_selector` method returns a
:py:class:`~pycommunicate.proxies.dom.element.ElementWrapper`. In this case, it is tracking the first thing with an id
of ``todo``. In our html file, that points to the ``<div>``. So this call will set todo_div equal to something that
represents... the todo div!

.. code-block:: python
   :linenos:
   :lineno-start: 4

   loading_message = self.html_wrapper.element_by_selector("#loadingBar")
   loading_message.delete()

The first line does similar things to the example above, so lets explain the second line. It calls ``loading_message``'s :py:meth:`delete` method,
which deletes the element. This effectively clears the "Loading..." message from the page.

.. code-block:: python
   :linenos:
   :lineno-start: 7

   for index in todo.todos:
       text = todo.todos[index]
       todo_page_div = todo_div.append_element_inside_self("div", "todo{}".format(index))
       text_p = todo_page_div.append_element_inside_self("p", "todoText{}".format(index))
       text_p.content.set(text)

So the loop goes through every todo in the :py:class:`TodoReader`. This class uses ids and a dictionary to store todos,
so we loop through the keys, which are the indices.

.. note::
   Although I could of used a list, this seemed easier to implement and keep track for removing entries, so I used a dictionary.

For each todo, get its text and store it in ``text``. Then, use the element creation function :py:meth:`~pycommunicate.proxies.dom.element.ElementWrapper.append_element_inside_self`
to create and get a ``<div>`` element with id ``todo{index}`` inside the ``todo_div``. The next call is very similar, only
calling it on ``todo_page_div`` and using it to create a ``<p>`` element with id ``todoText{index}`` instead.

The :py:attr:`~pycommunicate.proxies.dom.element.ElementWrapper.content` attribute is a wrapper for ``innerText``,
which can be used to get or set the text of an element. We use this to change the text of the new ``<p>`` element to
the text of the todo.

.. warning::
   The get functions of element properties block until the property is received, while the set() functions return as soon as the
   change is submitted to be sent. This means that calls to set() and then immediately after get() can return the wrong values.
   This will probably be changed in a later version, or an option added to block on the set() call.

.. code-block:: python
   :linenos:
   :lineno-start: 12

   button = todo_page_div.append_element_inside_self("button", "todoRemove{}".format(index))
   button.add_event_listener("click", self.make_handler(index))
   button.content.set("Remove")

Line 12 and 14 use already explained functions, so I'll detail the :py:meth:`~pycommunicate.proxies.dom.element.ElementWrapper.add_event_listener` method instead. This method
will attach an event to a js event. These are using the chrome and firefox names, not the IE ones. We use it here to attach
the button's click method to a dynamically generated event handler setup to destroy the todo server-side, and then use :py:meth:`~pycommunicate.proxies.dom.element.ElementWrapper.delete`
to remove it from the client-side.

Adding todos
------------

Add code to the load() method
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To do this, you need to add the following lines at the end of ``load()``:

.. code-block:: python
   :linenos:

   add_button = self.html_wrapper.element_by_selector("#add")
   add_button.add_event_listener("click", self.add_handler)

I've already explained above what this does, so let's go create that add_handler event handler.

The add_handler method
~~~~~~~~~~~~~~~~~~~~~~

The add_handler method will deal with when the user clicks the "Add" button.
Here's the code in it:

.. code-block:: python
   :linenos:

   text = "- " + self.html_wrapper.element_by_selector("#next").get_property("value")
   todo.add(text)
   self.html_wrapper.element_by_selector("#next").set_property("value", "")
   index = todo.wait_on(text)
   todo_div = self.html_wrapper.element_by_selector("#todo")
   todo_page_div = todo_div.append_element_inside_self("div", "todo{}".format(index))
   text_p = todo_page_div.append_element_inside_self("p", "todoText{}".format(index))
   text_p.content.set(text)
   button = todo_page_div.append_element_inside_self("button", "todoRemove{}".format(index))
   button.add_event_listener("click", self.make_handler(index))
   button.content.set("Remove")

Lines 5-11 are simply copied from the ``load()`` function, so look there for info on what these do.

Again, I'll go line by line.

.. code-block:: python
   :linenos:

   text = "- " + self.html_wrapper.element_by_selector("#next").get_property("value")

This will set text to "- " plus whatever is in the input field. The :py:meth:`~pycommunicate.proxies.dom.element.ElementWrapper.get_property` method will return whatever
the JS element defined by the :py:class:`~pycommunicate.proxies.dom.element.ElementWrapper` has for that name. The ``value`` property contains the content
of the input field.

Line 3 simply empties it using :py:meth:`~pycommunicate.proxies.dom.element.ElementWrapper.set_property`.

Lines 2 and 4 use the :py:class:`TodoReader` to add and retrieve the index for the new entry, and the rest is just as above.

Putting it all together
-----------------------


Your main.py file should now look like this:

.. literalinclude:: /examples/tutorial/tutorial.py
   :language: python
   :linenos:

If it looks like that (give or take some whitespace or comments) then you're good to go! Simply run it and connect to it
with the link in the console and watch your creation work!!

This is the end of the tutorial, but I'm sure you could do other stuff with this if you want.