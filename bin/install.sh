#!/bin/bash

if [ -s "$HOME/.nvm/nvm.sh" ]; then
    source "$HOME/.nvm/nvm.sh"
fi

npm install
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
