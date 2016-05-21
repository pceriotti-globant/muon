import os
import shlex

import muon
from muon.commands import AbstractCommand
from muon import docker


class Provision(AbstractCommand):
    """
    Run ansible on a container using the base image and save the results.

    Usage:
        provision
    """

    def execute(self):
        image = self.param('name')
        if not docker.image_exists(image):
            message = """
            Image `{image}` is not available. Ensure you run `muon create`
            before running this command.
            """
            muon.abort(message, image=image)

        command = shlex.split(self.param('noop_command'))
        with docker.run(image, command) as (cid, status):
            configfiles = (muon.DOCKERFILE, muon.PLAYBOOK, muon.INVENTORY)
            for filename in configfiles:
                if os.path.exists(filename):
                    docker.cp(cid, filename, muon.WORKDIR)

            roledir = muon.ROLEDIR % self.param('role')
            for pathname in self.param('ansible_dirs'):
                if os.path.exists(pathname):
                    docker.cp(cid, pathname, roledir)

            docker.commit(self.param('name'), cid, "Ansible update")

        command = shlex.split(self.param('provision_command'))
        rc = 0
        with docker.run(image, command) as (cid, status):
            rc = status
            docker.commit(self.param('name'), cid, "Ansible run")

        return rc
