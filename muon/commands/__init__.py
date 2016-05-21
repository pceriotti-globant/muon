"""
Usage:
    muon [-hv] <command> [<args>...]

Commands:
    setup       Create the scaffolding for a new role
    create      Create the base image used for testing
    provision   Run ansible on a container using the base image
    verify      Run testinfra on a container using the base image
    destroy     Destroy working image
    test        Run the full workflow
    run         Run a custom command

Options:
    -h --help     shows this screen
    -v --version  shows the version
"""

import importlib
import inspect
import json
import os
import subprocess
import sys

import docopt

import muon


class AbstractCommand(object):
    def __init__(self, command_args, global_args):
        self.args = docopt.docopt(inspect.getdoc(self), argv=command_args)
        self.args['<command>'] = self.__class__.__name__.lower()
        self.command_args = command_args

        if os.path.exists(muon.CONFIG):
            with open(muon.CONFIG, 'r') as fd:
                self.config = json.load(fd)
        else:
            self.config = {}

    def execute(self):
        raise NotImplementedError

    def update_config(self, changes):
        config = self.config.copy()
        config.update(changes)
        self.config = config

        with open(muon.CONFIG, 'w') as fd:
            json.dump(self.config, fd, sort_keys=True, indent=4)

    def param(self, key, default=None):
        value = self.config.get(key, default)
        if value is None:
            message = """
            Missing configuration key `{key}`.
            Please run `muon init` before running this command.
            """
            muon.abort(message, key=key)
        return value


def main():
    args = docopt.docopt(__doc__, options_first=True)
    command_mod = args.get('<command>')
    command_name = args.get('<command>').capitalize()
    command_args = {} if args.get('<args>') is None else args.pop('<args>')

    try:
        mod = 'muon.commands.%s' % (command_mod)
        importlib.import_module(mod)
        command_class = getattr(sys.modules[mod], command_name)
    except AttributeError:
        raise docopt.DocoptExit()

    try:
        command = command_class(command_args, args)
        sys.exit(command.execute())
    except OSError as e:
        message = "Error {e.errno} while accessing `{e.filename}`. {e.strerror}"
        muon.abort(message, e=e)
    except subprocess.CalledProcessError as e:
        message = "Error {e.returncode} while executing `{e.cmd}`"
        muon.abort(message, e=e)


if __name__ == '__main__':
    main()
