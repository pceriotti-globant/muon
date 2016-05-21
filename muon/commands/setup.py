import os
import time

import muon
from muon.commands import AbstractCommand
from muon import docker
from muon.template import Template


class Setup(AbstractCommand):
    """
    Creates the scaffolding for a new role intended for use with muon.

    Usage:
        setup [options]

    Options:
        -i --image <image>            Base docker image to use [default: centos:7].
        -n --name <name>              Name to use for the test image [default: {user}/{role}:latest].
        -d --dockerfile <dockerfile>  Dockerfile template to use [default: .muon/Dockerfile.j2].
        -y --inventory <inventory>    Inventory template to use [default: .muon/inventory.ini.j2].
        -p --playbook <playbook>      Playbook template to use [default: .muon/playbook.yml.j2].
    """

    def execute(self):
        image = self.args.get('--image')
        dockerfile = self.args.get('--dockerfile')
        inventory = self.args.get('--inventory')
        playbook = self.args.get('--playbook')

        name = self.args.get('--name').format(
            user=os.getlogin(),
            role=os.path.basename(os.getcwd()),
            epoch=time.time()
        )

        if not docker.image_exists(image):
            message = """
            Image `{image}` is not available. Ensure the name is correct
            and you did `docker pull {image}` before running this command.
            """
            muon.abort(message, image=image)

        if not os.path.exists(muon.WORKSPACE):
            os.mkdir(muon.WORKSPACE)

        config = {
            'image': image,
            'name': name,
            'role': os.path.basename(os.getcwd()),

            'ansible_dirs': ['defaults', 'files', 'handlers', 'meta', 'tasks', 'templates', 'vars'],
            'testinfra_dirs': ['tests'],

            'workflow': ['destroy', 'create', 'provision', 'verify', 'destroy'],

            'noop_command': '/bin/true',
            'verify_command': '/opt/ansible/bin/testinfra tests',
            'provision_command': '/opt/ansible/bin/ansible-playbook -i inventory.ini playbook.yml',
        }

        self.update_config(config)
        template = Template(config)
        template.render(dockerfile, muon.DOCKERFILE)
        template.render(inventory, muon.INVENTORY)
        template.render(playbook, muon.PLAYBOOK)

        return 0
