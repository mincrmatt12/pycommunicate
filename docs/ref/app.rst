CommunicateApp
==============

.. py:module:: pycommunicate.server.app.communicate


.. py:class:: CommunicateApp(self, web_port=8080, host='localhost', debug=False, maximum_handler_threads=10000, template_directory="templates")

   This is the main app instance, used to create and run a pycommunicate server. Its arguments are for configuration

   :param int web_port: The port to host the server on
   :param str host: The hostname to host on
   :param bool debug: Run with the debug server, never user in production
   :param int maximum_handler_threads: The size of the handler event pool. This may be removed in the future
   :param str template_directory: Relative path to the templates

   .. py:method:: set_secret_key(key)

      Sets the internal secret key

      .. danger::

         The secret key must be kept secret, for a truly random key use :py:func:`os.urandom`

      :param str key: The new secret key

   .. py:method:: add_controller(route, controller)

      Associates a :py:class:`~pycommunicate.server.bases.controller.ControllerFactory` with a route.

      .. warning::

         Any route starting with ``__pycommunicate/`` will not work, as this path is reserved for pycommunicate's
         internal routes.

      .. tip::

         Routes can contain variable parts, indicated like this: ``<name>`` where name is some name. You can also use
         integers, for that use ``<int:name>``.

      :param str route: The route
      :param pycommunicate.server.bases.controller.ControllerFactory controller: The controller factory to associate with the route

   .. py:method:: add_error_handler(code, controller)

      Associates a :py:class:`~pycommunicate.server.bases.controller.ControllerFactory` with an HTTP error code

      :param int code: The error code
      :param pycommunicate.server.bases.controller.ControllerFactory controller: The controller factory to associate the code with

      .. versionadded:: 0.0.7

   .. py:method:: run()

      Run the server, and block the current thread.