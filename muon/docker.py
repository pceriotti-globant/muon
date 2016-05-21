"""
Thin wrapper around the docker command line tool.
"""

import contextlib
import os
import subprocess
import tempfile
import time

DEVNULL = open(os.devnull, 'w')


def build(tag, dockerfile):
    """
    Build a tagged image using a custom Dockerfile.

    :param tag: Tag (name) for the image. ie: 'johndoe/example:latest'
    :type tag: str

    :param dockerfile: Path to the Dockerfile to be used. ie: '/my/custom/Dockerfile'
    :type dockerfile: str

    :return: 0 for success, other values for failure.
    :rtype: int

    Example::

        # build an image from a dockerfile on the current directory.
        dockerfile = os.path.join(os.getcwd, 'Dockerfile')
        rc = Docker.build('jhondoe/example:latest', dockerfile)
        if rc != 0:
            raise Exception('Failed to build image')
    """
    command = ['docker', 'build', '--tag', tag, '--file', dockerfile, '.']
    return subprocess.call(command)


def commit(image, container, message):
    """
    Commit the changes made on a container to an image.

    :param image: Image to be updated. ie: 'jhondoe/example:latest'
    :type image: str

    :param container: Source container identifier. ie: '1234567890AB'
    :type container: str

    :param message: Commit message. ie: 'I made some changes'
    :type message: str

    :raises subprocess.CalledProcessError: When the execution fails.

    :rtype: None

    Example::

        # Update nginx on an image
        image = 'jhondoe/nginx:latest'
        command = ['yum', 'update', '-q', '-y', 'nginx']
        with Docker.run(image, command) as (cid, status):
            if status == 0:
                Docker.commit(image, cid, "nginx updated")
    """
    message = "%s - %s" % (str(time.time()), message)
    command = ['docker', 'commit', '-m', message, container, image]
    subprocess.check_call(command, stdout=DEVNULL, stderr=DEVNULL)


def cp(container, src, dst):
    """
    Copy local files to a container.

    :param container: Destination container identifier. ie: '1234567890AB'
    :param type: str

    :param src: Local source path. ie: '/my/local/path'
    :type src: str

    :param dst: Remove destination path. ie: '/my/container/path'
    :type dst: str

    :raises subprocess.CalledProcessError: When the execution fails.

    :rtype: None

    Example::

        # Update root's authorized_keys with your own SSH public key
        try:
            source = os.path.expanduser('~/.ssh/id_rsa.pub')
            destination = '/root/.ssh/authorized_keys'
            Docker.cp(cid, source, destination)
        except CalledProcessError as e:
            raise Exception('Failed to update authorized_keys')
    """
    command = ['docker', 'cp', src, '%s:%s' % (container, dst)]
    subprocess.check_call(command, stdout=DEVNULL, stderr=DEVNULL)


def image_exists(image):
    """
    Check if an image is available on the docker server.

    :param image: The image name to be checked for. ie: 'centos:7'
    :type image: str

    :return: True if the image is available, False otherwise
    :rtype: bool

    Example::

        # if an image is available build a container using it.
        if Docker.image_exists('centos:7'):
            Docker.build('jhondoe/example:latest', '/my/custom/Dockerfile')
        else:
            raise Exception('please run `docker pull centos:7` before this')
    """
    command = ['docker', 'images', '-q', image]
    output = subprocess.check_output(command)
    return 0 != len(output)


def rm(container):
    """
    Remove a container.

    :param container: Target's container identifier. ie: '1234567890AB'
    :type container: str

    :return: 0 for success, other values for failure.
    :rtype: int

    Example::

        rc = Docker.rm('1234567890AB')
        if rc == 0:
            print "Container 1234567890AB removed"
    """
    command = ['docker', 'rm', container]
    return subprocess.call(command, stdout=DEVNULL, stderr=DEVNULL)


def rmi(image):
    """
    Remove an image.

    :param image: Target's image name. ie: 'jhondoe/example:latest'
    :type image: str

    :return: 0 for success, other values for failure.
    :rtype: int

    Example::

        rc = Docker.rmi('jhondoe/example:latest')
        if rc == 0:
            print "Image jhondoe/example:latest removed"
    """
    command = ['docker', 'rmi', image]
    return subprocess.call(command, stdout=DEVNULL, stderr=DEVNULL)


@contextlib.contextmanager
def run(image, arguments=[]):
    """
    Run a set of commands inside an image and keep its container identifier
    (cid) and return code (status) for future commands to use.

    After the commands run (or the context end due to an error) the
    container *will be deleted* and its cidfile removed.

    :param image: Base image used to run the command. ie: 'centos:7'
    :type image: str

    :param arguments: Command in a format supported by both, `docker run`
        and `subprocess.call`. Usually a shell splitted list of string.
        ie: (['ls', '-lR'])
    :type arguments: list

    :rtype: None

    Example::

        # Copy a directory to a container after updating its packages.
        command = ['yum', 'update', '-q', '-y']
        with Docker.runcontext('centos:7', command) as (cid, status):
            # commit the changes if the update was successful
            if status == 0:
                Docker.commit(cid, 'Packages updated')
    """
    cid = None
    status = None

    cidfile = tempfile.NamedTemporaryFile(bufsize=0)
    cidfile.close()

    try:
        command = ['docker', 'run', "--cidfile", cidfile.name, '--tty', '--interactive']
        command.append(image)
        command.extend(arguments)

        status = subprocess.call(command)

        with open(cidfile.name, 'r') as fd:
            cid = fd.read()

        yield (cid, status)
    finally:
        if cid:
            rm(cid)
        try:
            os.unlink(cidfile.name)
        except OSError:
            pass
