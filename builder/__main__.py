from os.path import dirname, join, normpath
import sys

from .commands import CommandError, CheckPrereq, Download, Untar
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

    # TODO:
    # Because we're cross-compiling, we need native versions of some LLVM/Clang
    # binaries. Default to latest versions under /usr/bin
    # Find /usr/bin/llvm-tblgen*
    # Find /usr/bin/clang-tblgen*

    try:
        executor.execute([
            CheckPrereq('cmake --version', package='cmake'),
            CheckPrereq('emcc --version', custom_message=emscripten_message),
            CheckPrereq('em++ --version', custom_message=emscripten_message),
            Download(llvm_releases + 'llvm-%s.src.tar.xz' % version),
            Untar('llvm'),
            Download(llvm_releases + 'cfe-%s.src.tar.xz' % version),
            Untar('llvm/tools/clang'),
            Download(llvm_releases + 'clang-tools-extra-%s.src.tar.xz' % version),
            Untar('llvm/tools/clang/tools/extra'),
        ])
    except CommandError as e:
        # CommandError indicates that the command did its own error
        # handling.  Report failure, but don't show a stack trace.
        sys.exit(1)

    # TODO:
    # Add needed patches

    # TODO:
    # mkdir -p build
    # cd build && CXX=em++ CC=emcc cmake \
    #     -DCMAKE_TOOLCHAIN_FILE=$(EMSCRIPTEN)/cmake/Modules/Platform/Emscripten.cmake \
    #     -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release \
    #     -DLLVM_TABLEGEN=$(LLVM_TABLEGEN) -DCLANG_TABLEGEN=$(CLANG_TABLEGEN) ../llvm
    # cd build && make


main()
