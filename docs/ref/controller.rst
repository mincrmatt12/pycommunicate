Controller and ControllerFactory
================================

.. py:module:: pycommunicate.server.bases.controller

.. py:class:: ControllerFactory

   This class is used to define how a :py:class:`Controller` should be created. Its methods are all chainable,
   or in other words, all return the instance. The constructor has no arguments

   .. py:method:: add_view(view)

      Adds a py:class:`pycommunicate.server.bases.views.View` to the controller factory's view list.

      .. warning::

         Adding the same view twice can cause issues

      :param pycommunicate.server.bases.views.View view: The view class to add

   .. py:method:: set_default_view(view)

      Sets the default view for the controller factory. The default view is the one that is shown initially.

      .. warning::

         The client will crash with a 500 server error if this is not set.

      :param pycommunicate.server.bases.views.View view: The view class to set as default.

   .. py:method:: with_before_connect(before_connect)

      Sets the before_connect function. This is called as soon as a request comes in for the page, and should be
      used to do something before a page loads.

      before_connect takes one argument, an instance of :py:class:`pycommunicate.proxies.context.CallCTX`. This CallCTX
      contains one function, ``abort``, which when called will interrupt the request and send back the error code passed
      to it.

      :param function before_connect: The before_connect function. See above for signature


.. py:class:: Controller

   The Controller class handles one url, or route. It contains multiple :py:class:`pycommunicate.server.bases.views.View`s
   and manages switching between them.

   .. warning::

      Do not try and create :py:class:`Controller` instances on your own. Use :py:class:`ControllerFactory` for that instead.

   .. py:attribute:: route_data

      This contains the values of the variable parts in the route. See :py:meth:`pycommunicate.server.app.communicate.CommunicateApp.add_controller`
      for more information on variable route parts.

   .. py:attribute:: d

      This is the data object, a simple dictionary that use can use to store data across multiple views. It is reset every
      request, for full sessions across requests use ``user.session`` instead.

   .. py:attribute:: user

      An instance of :py:class:`pycommunicate.server.app.usertracker.User` of which this controller is currently servicing.
      Use its ``session`` attribute for proper sessions.

   .. py:attribute:: special_return_handler

      If this is not None, then whatever this function returns will be sent directly to flask as the response. Use with caution.

      .. versionadded:: 0.0.7

   .. py:method:: change_view(new_view_index)

      Change the active view to the index provided. View indices start at 0 and increase in the order you added them in
      the controller factory.

      .. note::

         This will only do anything if the page has the pycommunicate JS libraries loaded. This function
         will not work from within a ``render()`` function.

      :param int new_view_index: The new view index to switch to.

   .. py:method:: redirect(location)

      If called from a child view's ``render()`` function, this will change the special_return_handler to a function
      that returns a redirect to the location. Otherwise, it signals the page to redirect elsewhere.

      .. note::

         This will only do anything outside of ``render()`` if the page has the pycommunicate JS libraries loaded.

      :param str location: The url to redirect to.