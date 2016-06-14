HTMLWrapper and ElementWrapper
==============================

.. warning::
   All the methods documented here require the target document to include the JS libraries.

.. py:module:: pycommunicate.proxies.dom.html

.. py:class:: HTMLWrapper

   This class allows you to get :py:class:`~pycommunicate.proxies.dom.element.ElementWrapper` instances, and check for
   their existance.

   Every controller and view has one, and these are not created by the user.

   .. py:method:: exists(selector)

      Ask the browser whether an element matching the given selector exists.
      This method will block.

      :param str selector: The selector to check
      :return: Whether or not the target element exists
      :rtype: bool

      .. versionchanged:: 0.0.8
         Renamed to exists.

   .. py:method:: element(selector)

      First call :py:meth:`~HTMLWrapper.exists` and if it returns True return an :py:class:`~pycommunicate.proxies.dom.element.ElementWrapper`
      instance tracking the element defined by selector. Otherwise return None

      :param str selector: The selector for the element
      :return: An :py:class:`~pycommunicate.proxies.dom.element.ElementWrapper` instance tracking the given selector or None if none is found.
      :rtype: pycommunicate.proxies.dom.element.ElementWrapper

      .. versionchanged::
         Renamed to element.


.. py:module:: pycommunicate.proxies.dom.element

.. py:class:: ElementWrapper

   This class tracks an element by selector, and provides many utility functions and properties for it.

   These are created by :py:class:`~pycommunicate.proxies.dom.html.HTMLWrapper` and should not be created manually.

   .. py:method:: prop(name, value=None)

      Wrapper around :py:meth:`~ElementWrapper.get_property()` and :py:meth:`~ElementWrapper.set_property()`. This is
      part of the new chainable API.

      Calling this without value or with value set to None will result in getting the property and returning its value.
      Calling this with a value will set the property to value, and return the element. You can chain calls in this way.

      :param str name: The name of the property to get/set
      :param object name: The value to set to, if None do a get.

      .. versionadded:: 0.0.8

   .. py:method:: get_property(property_name)

      Get a python representation of JS property named ``property_name``.
      This method will block

      :param str property_name: The name of the JS property to get
      :return: The value of the property, coverted to python types where possible

   .. py:method:: set_property(property_name, value)

      Set the JS property named ``property_name`` to a JS representation of ``value``

      .. warning::

         The get methods block until the value is received, but the set methods do not block at all. This can
         cause some odd things, like this:

         .. code-block:: python

            >>> my_element.set_property('value', 5)
            >>> my_element.get_property('value')
            None
            >>> # ???

         There is currently no way to prevent this, but this may change in a future version.

      :param str property_name: The name of JS property to set
      :param object value: The value to set it to
      :return: None

   .. py:method:: add_event_listener(event_name, handler)

      Add an event handler for the given JS event. The names are in chrome/firefox format, not IE.
      Some examples of events are ``click``, ``focus``, and ``blur``.

      ``handler()`` takes no parameters.

      :param str event_name: The JS name of the event
      :param function handler: An event handler function

   .. note::

      The next two methods are probably going to be removed in a later release, but are still valid now.

   .. py:method:: append_element_after_self(element_type, id)

      Add a new element of type ``element_type`` with **unique** id ``id`` after this element, and return it.

      :param str element_type: The type of the element, e.g. ``p`` or ``div``
      :param str id: The id to assign to the element. Must be unique.
      :return: The new element
      :rtype: pycommunicate.proxies.dom.element.ElementWrapper

   .. py:method:: append_element_inside_self(element_type, id)

      Add a new element of type ``element_type`` with **unique** id ``id`` as a child of this element, and return it.

      :param str element_type: The type of the element, e.g. ``p`` or ``div``
      :param str id: The id to assign to the element. Must be unique.
      :return: The new element
      :rtype: pycommunicate.proxies.dom.element.ElementWrapper

   .. py:method:: delete()

      Delete this element.

      .. warning::

         After calling :py:meth:`~ElementWrapper.delete`, the instance should no longer be used.

   The following are wrappers for properties. They are actually descriptors, so you can just use them.

   .. versionchanged:: 0.0.8
      Removed old ``get()`` and ``set()`` api

   .. py:attribute:: content

      Wrapper for ``innerText``

   The following are properties that have more than one value. These use the following syntax (using
   :py:attr:`~ElementWrapper.style` as an example)

   .. code-block:: python

      >>> my_element.style['marginTop']
      '123px'
      >>> my_element.style['marginTop'] = '456px'

   .. py:attribute:: style

      Wrapper for ``style``
