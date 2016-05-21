from muon.commands import AbstractCommand
from muon import docker


class Destroy(AbstractCommand):
    """
    Destroy working image.

    Usage:
        destroy
    """

    def execute(self):
        image = self.param('name')
        docker.rmi(image)
        return 0
