import os
import os.path
import shutil
import subprocess

from .util import download

class Command(object):
    def set_config(self, config):
        self.config = config

    def check(self):
        return False

    def rollback(self):
        pass

    def set_input(self, new_input):
        self.input = new_input

    def get_output(self):
        return None

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

