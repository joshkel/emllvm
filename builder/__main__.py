from os.path import dirname, join, normpath

from .commands import Download, Untar
from .executor import Executor

def make_executor():
    executor = Executor()
    executor.config.root = normpath(join(dirname(__file__), '..'))
    return executor

def main():
    version = '3.9.1'
    llvm_releases = 'http://llvm.org/releases/%s/' % version

    executor = make_executor()

    executor.execute([
        Download(llvm_releases + 'llvm-%s.src.tar.xz' % version),
        Untar('llvm'),
        Download(llvm_releases + 'cfe-%s.src.tar.xz' % version),
        Untar('llvm/tools/clang'),
        Download(llvm_releases + 'clang-tools-extra-%s.src.tar.xz' % version),
        Untar('llvm/tools/clang/tools/extra'),
    ])

main()
