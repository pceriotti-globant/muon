import os
import re
import sys
import textwrap

from pbr import version

try:
    version_info = version.VersionInfo('muon')
    __version__ = version_info.release_string()
except AttributeError:
    __version__ = None


WORKSPACE = '.muon'
CONFIG = os.path.join(WORKSPACE, 'config.json')
DOCKERFILE = os.path.join(WORKSPACE, 'Dockerfile')
INVENTORY = os.path.join(WORKSPACE, 'inventory.ini')
PLAYBOOK = os.path.join(WORKSPACE, 'playbook.yml')
WORKDIR = '/muon'
ROLEDIR = os.path.join(WORKDIR, 'roles', '%s')


def abort(message, **kwargs):
    message = textwrap.dedent(message.format(**kwargs)).strip()
    message = re.sub('\s+', ' ', message)
    message = re.sub('\.\s+', '.\n  ', message)
    sys.stderr.write("\n  " + message + "\n\n")
    sys.exit(1)
