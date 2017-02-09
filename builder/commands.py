import os
from os.path import basename, exists, join

from .util import download

class Command(object):
    def set_config(self, config):
        self.config = config

class Download(Command):
    def __init__(self, url):
        self.url = url

    def download_dir(self):
        return join(self.config.root, 'downloads')

    def local_path(self):
        return join(self.config.root, 'downloads', basename(self.url))

    def check(self):
        return exists(self.local_path())

    def execute(self):
        os.makedirs(self.download_dir(), exist_ok=True)
        download(self.url, self.local_path())

    def rollback(self):
        try:
            os.unlink(self.local_path())
        except OSError:
            pass

