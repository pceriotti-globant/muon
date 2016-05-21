import importlib
import sys

from muon.commands import AbstractCommand


class Test(AbstractCommand):
    """
    Run the full workflow (destroy, create, provision, verify, destroy)

    Usage:
        test
    """

    def execute(self):
        for command in self.param('workflow'):
            mod = 'muon.commands.%s' % (command)
            importlib.import_module(mod)

            command_class = getattr(sys.modules[mod], command.capitalize())
            command = command_class({}, {})
            rc = command.execute()
            if rc != 0:
                return rc
        return 0
