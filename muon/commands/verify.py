import os
import shlex

import muon
from muon.commands import AbstractCommand
from muon import docker


class Verify(AbstractCommand):
    """
    Run testinfra on a container using the base image and save the results.

    Usage:
        verify
    """

    def execute(self):
        image = self.param('name')
        if not docker.image_exists(image):
            message = """
            Image `{image}` is not available. Ensure you run `muon create`
            and `muon provision` before running this command.
            """
            muon.abort(message, image=image)

        command = shlex.split(self.param('noop_command'))
        with docker.run(image, command) as (cid, status):
            for pathname in self.param('testinfra_dirs'):
                if os.path.exists(pathname):
                    docker.cp(cid, pathname, muon.WORKDIR)

            docker.commit(self.param('name'), cid, "TestInfra update")

        command = shlex.split(self.param('verify_command'))
        rc = 0
        with docker.run(image, command) as (cid, status):
            rc = status

        return rc
