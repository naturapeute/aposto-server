import os
from typing import Dict, List

import ujson
from dotenv import load_dotenv
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from doc import generate_schema

from routes import routes

load_dotenv()
SEND_IN_BLUE_API_KEY = os.getenv("SEND_IN_BLUE_API_KEY")

with open("config.json", "r") as configData:
    ENV = os.getenv("ENV")
    fullConfig: Dict[str, Dict[str, str]] = ujson.load(configData)
    config: Dict[str, str] = fullConfig["PROD"] if ENV == "PROD" else fullConfig["DEV"]

middleware: List[Middleware] = [
    Middleware(
        CORSMiddleware,
        allow_origins=[config["apostoAppURL"], config["apostoBetaURL"]],
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type", "Accept"],
    ),
]

app: Starlette = Starlette(debug=True, middleware=middleware, routes=routes)
app.state.SEND_IN_BLUE_API_KEY = os.getenv("SEND_IN_BLUE_API_KEY")

for key in config.keys():
    setattr(app.state, key, config[key])

generate_schema(app)
