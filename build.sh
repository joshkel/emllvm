#!/bin/bash

set -e

cd "$(dirname "$0")"

if ! which emcc >& /dev/null; then
    if [ -d emsdk-portable ]; then
        . emsdk-portable/emsdk_env.sh
    fi
fi

python3 -m builder
