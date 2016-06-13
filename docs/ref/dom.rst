HTMLWrapper and ElementWrapper
==============================

.. warning::
   All the methods documented here require the target document to include the JS libraries.

.. py:module:: pycommunicate.proxies.dom.html

.. py:class:: HTMLWrapper

   This class allows you to get :py:class:`~pycommunicate.proxies.dom.element.ElementWrapper` instances, and check for
   their existance.

   Every controller and view has one, and these are not created by the user.

   .. py:method:: element_exists(selector)

      Ask the browser whether an element matching the given selector exists.
      This method will block.

      :param str selector: The selector to check
      :return: Whether or not the target element exists
      :rtype: bool

   .. py:method:: element_by_selector(selector)

      First call :py:meth:`~HTMLWrapper.element_exists` and if it returns True return an :py:class:`~pycommunicate.proxies.dom.element.ElementWrapper`
      instance tracking the element defined by selector. Otherwise return None

      :param str selector: The selector for the element
      :return: An :py:class:`~pycommunicate.proxies.dom.element.ElementWrapper` instance tracking the given selector or None if none is found.
      :rtype: pycommunicate.proxies.dom.element.ElementWrapper

.. py:module:: pycommunicate.proxies.dom.element

.. py:class:: ElementWrapper

   This class tracks an element by selector, and provides many utility functions and properties for it.

   These are created by :py:class:`~pycommunicate.proxies.dom.html.HTMLWrapper` and should not be created manually.

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



