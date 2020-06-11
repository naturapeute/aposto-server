#!/bin/bash

source venv/bin/activate

uvicorn --host 0.0.0.0 --port 8080 --reload app:app
