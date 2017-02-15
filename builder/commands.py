import os
import os.path
import shutil
import subprocess
import sys

from .util import download


class CommandError(Exception):
    pass


class Command(object):
    def set_config(self, config):
        self.config = config

    def check(self):
        """Checks if a command has already been done."""
        return False

    def execute(self):
        """Executes the command."""
        raise NotImplementedError

    def rollback(self):
        """Rolls back / undoes a (possibly partially) completed command."""
        pass

    def set_input(self, new_input):
        """Primitive pipeline support: set this "input" (details are command-
        specific) to the given value."""
        self.input = new_input

    def get_output(self):
        """Primitive pipeline support: gets the "output" (details are command-
        specific)."""
        return None


class CheckPrereq(Command):
    def __init__(self, command, custom_message=None, package=None):
        self.command = command
        self.custom_message = custom_message
        self.package = package

    def execute(self):
        try:
            subprocess.check_call(self.command, shell=True)
        except subprocess.SubprocessError as e:
            print('Missing prerequisite: Failed to execute %s' % self.command, file=sys.stderr)
            if self.custom_message:
                print(self.custom_message, file=sys.stderr)
            if self.package:
                print(('Try running "brew install {pkg}", "apt-get install {pkg}", ' +
                       'or similar.').format({'pkg': self.package}), file=sys.stderr)
            raise CommandError


class Download(Command):
    def __init__(self, url):
        self.url = url

    def download_dir(self):
        return os.path.join(self.config.root, 'downloads')

    def local_path(self):
        return os.path.join(self.download_dir(), os.path.basename(self.url))

    def check(self):
        return os.path.exists(self.local_path())

    def execute(self):
        os.makedirs(self.download_dir(), exist_ok=True)
        download(self.url, self.local_path())

    def rollback(self):
        os.unlink(self.local_path())

    def get_output(self):
        return self.local_path()


class Untar(Command):
    def __init__(self, local_dir):
        self.local_dir = local_dir

    def local_path(self):
        return os.path.join(self.config.root, self.local_dir)

    def check(self):
        return os.path.isdir(self.local_path())

    def execute(self):
        subprocess.check_call([
            'tar', '-xvf', self.input,
            '-C', os.path.dirname(self.local_path()),
            '--transform', r"s/^[^\/]*/%s/" % os.path.basename(self.local_path())])

    def rollback(self):
        shutil.rmtree(self.local_path())
