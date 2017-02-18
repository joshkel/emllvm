# emllvm

[LLVM](http://llvm.org/) and [Clang](https://clang.llvm.org/) ported to
[Emscripten](http://emscripten.org/)

## Instructions

1. Install prerequisites.
   * [Emscripten](http://emscripten.org/)
   * Clang - emllvm has been tested against Clang 3.9 and currently assumes that Clang binaries are available under `/usr/bin` and has been tested against Clang 3.9.
   * CMake - Currently, version 3.4.3 or newer is required.  See [LLVM documentation](http://llvm.org/docs/CMake.html) for details.
2. Run the build script.

    ```
    cd emllvm
    python3 -m builder
    ```

## Further reading

* http://llvm.org/docs/HowToCrossCompileLLVM.html
* https://github.com/kripken/llvm.js - may be outdated, but it has some useful info
