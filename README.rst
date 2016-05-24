Muon
====

`Muon <http://muon-tool.rtfd.io>`_ is a tool designed to help in the
development of `Ansible <https://www.ansible.com>`_ roles.

It uses `Docker <https://www.docker.com>`_ containers instead of virtual
machines to provide the fastest workflow possible.

The verification part is handled by
`Testinfra <http://testinfra.readthedocs.io/en/latest/>`_, a plugin for the
`Pytest <http://pytest.org>`_ test engine.


Quick Start
-----------

Install muon using pip:

.. code-block:: bash

  $ pip install muon

Create a new role:

.. code-block:: bash

  $ ansible-galaxy init shiny_new_role
  $ cd shiny_new_role
  $ muon setup

Iterate over your new functiontionality:

.. code-block:: bash

  $ muon provision

Iterate over your tests:

.. code-block:: bash

  $ muon verify

Run a complete cycle on a clean environment:

.. code-block:: bash

  $ muon test


Documentation
-------------

http://muon-tool.rtfd.io


License
-------

MIT
