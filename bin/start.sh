#!/bin/bash

source venv/bin/activate
export DISPLAY=':99.0'
Xvfb :99 -screen 0 1024x768x24 > /dev/null 2>&1 &

if [ -s "$HOME/.nvm/nvm.sh" ]; then
    source "$HOME/.nvm/nvm.sh"
fi

uvicorn --host 0.0.0.0 --port 8080 --workers 4 app:app
