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

    # TODO:
    # Because we're cross-compiling, we need native versions of some LLVM/Clang
    # binaries. Default to latest versions under /usr/bin
    # Find /usr/bin/llvm-tblgen*
    # Find /usr/bin/clang-tblgen*
    # Verify cmake --version, emcc --version, em++ --version

    executor.execute([
        Download(llvm_releases + 'llvm-%s.src.tar.xz' % version),
        Untar('llvm'),
        Download(llvm_releases + 'cfe-%s.src.tar.xz' % version),
        Untar('llvm/tools/clang'),
        Download(llvm_releases + 'clang-tools-extra-%s.src.tar.xz' % version),
        Untar('llvm/tools/clang/tools/extra'),
    ])

    # TODO:
    # Add needed patches

    # TODO:
    # mkdir -p build
    # cd build && CXX=em++ CC=emcc cmake -DCMAKE_TOOLCHAIN_FILE=$(EMSCRIPTEN)/cmake/Modules/Platform/Emscripten.cmake -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release -DLLVM_TABLEGEN=$(LLVM_TABLEGEN) -DCLANG_TABLEGEN=$(CLANG_TABLEGEN) ../llvm
    # cd build && make

main()
