Usage
=====

`Muon <http://muon-tool.rtfd.io>`_ is a tool designed to help in the
development of `Ansible <https://www.ansible.com>`_ roles.

It uses `Docker <https://www.docker.com>`_ containers instead of virtual
machines to provide the fastest workflow possible.

The verification part is handled by
`Testinfra <http://testinfra.readthedocs.io/en/latest/>`_, a plugin for the
`Pytest <http://pytest.org>`_ test engine.

To start using `Muon <http://muon-tool.rtfd.io>`_ with your role you
need to run :class:`muon setup <muon.commands.setup.Setup>` on the
role's directory.

:class:`muon setup <muon.commands.setup.Setup>` will create a directory
called ``.muon`` with a configuration file and some templates. Every time
you change the templates you will need to run this command again to rebuild the
final files.

The files you will be most interested into modify are:

* ``.muon/Dockerfile.j2`` `Docker <https://www.docker.com>`_ configuration
  template. The base image will be generated from it.
* ``.muon/inventory.ini.j2`` `Ansible <https://www.ansible.com>`_ inventory
  template. You can change `Ansible <https://www.ansible.com>`_ options from
  here.
* ``.muon/playbook.yml.j2`` `Ansible <https://www.ansible.com>`_ playbook
  template. The playbook to run will be generated from it.

All templates are processed using `Jinja <http://jinja.pocoo.org>`_ template
engine.

The variables available to the templates are taken from
``.muon/config.json``. There you can change how
`Testinfra <http://testinfra.readthedocs.io/en/latest/>`_ and
`Ansible <https://www.ansible.com>`_ are executed.

The next step is to run
:class:`muon create <muon.commands.create.Create>`. It will create a
base image. This image will be where all your work will be saved.

The next two steps are the core of the tool.
:class:`muon provision <muon.commands.provision.Provision>` which run
`Ansible <https://www.ansible.com>`_ on the image and
:class:`muon verify <muon.commands.verify.Verify>` which run
`Testinfra <http://testinfra.readthedocs.io/en/latest/>`_.

:class:`muon provision <muon.commands.provision.Provision>` will copy
your role to the image, the inventory and the playbook. Then it will run
``ansible-playbook``, show you the result and save your changes to the image.

:class:`muon verify <muon.commands.verify.Verify>` will copy your tests
to the image and run `Testinfra <http://testinfra.readthedocs.io/en/latest/>`_
and show you the result.

You can use :class:`muon run <muon.commands.run.Run>` to run custom
commands on the image, by default it will run ``/bin/bash`` to give you access
to the full environment. If you need to pass options to your command prefix it
with ``-- (double dash)`` to indicate its not an option for
`Muon <http://muon-tool.rtfd.io>`_. As before any changes you made on
the image will be saved.

To destroy your image you should do
:class:`muon destroy <muon.commands.destroy.Destroy>`.

If you want to run a fully cycle for continous integration purposes you can
do it with :class:`muon test <muon.commands.test.Test>`. This command
will run the following workflow in sequence aborting if anything fails.

* :class:`muon destroy <muon.commands.destroy.Destroy>`
* :class:`muon create <muon.commands.create.Create>`
* :class:`muon provision <muon.commands.provision.Provision>`
* :class:`muon verify <muon.commands.verify.Verify>`
* :class:`muon destroy <muon.commands.destroy.Destroy>`
