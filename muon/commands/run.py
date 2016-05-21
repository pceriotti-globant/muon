import muon
from muon.commands import AbstractCommand
from muon import docker


class Run(AbstractCommand):
    """
    Run a command inside your working image.

    Usage:
        run [<shell>]...
    """

    def execute(self):
        image = self.param('name')
        if not docker.image_exists(image):
            message = """
            Image `{image}` is not available. Ensure you run
            `muon create` before running this command.
            """
            muon.abort(message, image=image)

        shell = self.args.get('<shell>')
        if shell is None:
            shell = ['/bin/bash']
        elif shell[0] == '--':
            shell.pop(0)

        rc = 0
        with docker.runcontext(image, shell) as (cid, status):
            rc = status
            docker.commit(self.param('name'), cid, "Exec run")

        return rc
