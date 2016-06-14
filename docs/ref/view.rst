View
====

.. py:module:: pycommunicate.server.bases.views

.. py:class:: View

   The base view class. This is designed to be subclassed to create your own views.

   Again, don't try and create these manually.

   .. py:attribute:: controller

      The current :py:class:`~pycommunicate.server.bases.controller.Controller` instance this view is bound to.

   .. py:attribute:: html_wrapper

      An instance of :py:class:`~pycommunicate.proxies.dom.html.HTMLWrapper`.

   .. py:method:: render()

      This method *must* be overridden, otherwise viewing it will result in a 500 server error.
      It should return the content of the page, usually as an html file.
