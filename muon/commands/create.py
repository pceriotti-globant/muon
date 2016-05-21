import muon
from muon.commands import AbstractCommand
from muon import docker


class Create(AbstractCommand):
    """
    Create the base image used for testing

    Usage:
        create
    """

    def execute(self):
        return docker.build(self.param('name'), muon.DOCKERFILE)
