from os.path import dirname, join, normpath
import sys

from .commands import CommandError, CheckPrereq, Configure, Download, FindClang, Make, \
    MakeBuildDirectory, Patch, Untar
from .executor import Executor

emscripten_message = (
    'Please download and install the Emscripten SDK, and "source emsdk_env.sh"\n'
    'if needed.  For more information: \n'
    'http://kripken.github.io/emscripten-site/docs/getting_started/downloads.html'
)


def make_executor():
    executor = Executor()
    executor.config.root = normpath(join(dirname(__file__), '..'))
    return executor


def main():
    version = '3.9.1'
    llvm_releases = 'http://llvm.org/releases/%s/' % version

    executor = make_executor()

    try:
        executor.execute([
            CheckPrereq('cmake --version', package='cmake'),
            CheckPrereq('emcc --version', custom_message=emscripten_message),
            CheckPrereq('em++ --version', custom_message=emscripten_message),
            FindClang(),
            Download(llvm_releases + 'llvm-%s.src.tar.xz' % version),
            Untar('llvm'),
            Download(llvm_releases + 'cfe-%s.src.tar.xz' % version),
            Untar('llvm/tools/clang'),
            Download(llvm_releases + 'clang-tools-extra-%s.src.tar.xz' % version),
            Untar('llvm/tools/clang/tools/extra'),
            Patch('llvm-%s.patch' % version),
            MakeBuildDirectory(),
            Configure(),
            Make()
        ])
    except CommandError as e:
        # CommandError indicates that the command did its own error
        # handling.  Report failure, but don't show a stack trace.
        sys.exit(1)


main()
