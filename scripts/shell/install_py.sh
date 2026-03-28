#!/bin/bash

export DEBIAN_FRONTEND=noninteractive

if command -v python3.14 >/dev/null 2>&1 || python3 --version 2>&1 | grep -q "3.14"; then
    PY_EXISTS=1
fi

if ! command -v uv >/dev/null 2>&1; then
    curl -LsSf https://astral.sh/uv/install.sh | sh >/dev/null 2>&1
    source $HOME/.cargo/env >/dev/null 2>&1
    export PATH="$HOME/.cargo/bin:$PATH"
fi

if [ -z "$PY_EXISTS" ]; then
    if [ "$EUID" -eq 0 ] || sudo -n true >/dev/null 2>&1; then
        if [[ "$OSTYPE" == "darwin"* ]]; then
            command -v brew >/dev/null 2>&1 || /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" >/dev/null 2>&1
            brew install python@3.14 >/dev/null 2>&1
        elif command -v apt-get >/dev/null 2>&1; then
            sudo apt-get update -y >/dev/null 2>&1
            sudo apt-get install -y software-properties-common >/dev/null 2>&1
            sudo add-apt-repository -y ppa:deadsnakes/ppa >/dev/null 2>&1
            sudo apt-get install -y python3.14 python3.14-venv >/dev/null 2>&1
        fi
    fi

    uv python install 3.14 >/dev/null 2>&1
fi

uv pip install --quiet requests >/dev/null 2>&1