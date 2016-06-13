User
====

.. py:module:: pycommunicate.server.app.usertracker

.. py:class:: User

   This class represents a unique session to the server, known as a user. It also tracks the session and their current
   controller.

   These are not to be created manually.

   .. py:attribute:: id_

      The unique id for this user.

      .. danger::

         This information can be used to impersonate someone else on your website.

   .. py:attribute:: request_id

      The current request id. This changes every page load.

   .. py:attribute:: session

      The user's session. This is a dict

   .. py:attribute:: active_controller

      The active controller for this user

   .. py:attribute:: socket_connected

      Whether or not the JS lib has connected to this user.