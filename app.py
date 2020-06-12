import os
from pathlib import Path
from typing import Dict, List

import ujson
import yaml
from dotenv import load_dotenv
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.schemas import SchemaGenerator
from swagger_ui import api_doc

from models import Invoice
from routes import routes

load_dotenv()
SEND_IN_BLUE_API_KEY = os.getenv("SEND_IN_BLUE_API_KEY")

with open("config.json", "r") as configData:
    ENV = os.getenv("ENV")
    fullConfig: Dict[str, Dict[str, str]] = ujson.load(configData)
    config: Dict[str, str] = fullConfig["PROD"] if ENV == "PROD" else fullConfig["DEV"]

invoice_schema: dict = Invoice.schema()
definitions_schema: dict = invoice_schema["definitions"]
invoice_schema.pop("definitions", None)

schemas: SchemaGenerator = SchemaGenerator(
    {
        "openapi": "3.0.0",
        "info": {"title": "Aposto API", "version": "1.0"},
        "servers": [],
        "components": {
            "schemas": {
                "Invoice": invoice_schema,
                "JSONError": {
                    "description": "An error occurring when the request body contains wrongly formatted JSON",
                    "properties": {
                        "json_error": {
                            "description": "An error message describing the JSON error. The syntax error position is provided",
                            "type": "string",
                        }
                    },
                },
                "ValidationError": {
                    "description": "An error occurring when the invoice content is incorrect",
                    "properties": {
                        "loc": {
                            "description": "The field sequence raising an error. `['author','name']` corresponds to `author.name`",
                            "type": "array",
                            "items": {"type": "string"},
                        },
                        "msg": {
                            "description": "The validation error message",
                            "type": "string",
                        },
                        "type": {
                            "description": "The type of validation error",
                            "type": "string",
                        },
                    },
                },
                "SendinBlueError": {
                    "description": "An error occurring when sending an email with SendinBlue service has failed",
                    "properties": {
                        "code": {"description": "An error code", "type": "string"},
                        "message": {
                            "description": "A readable message associated with the failure",
                            "type": "string",
                        },
                    },
                },
            }
        },
        "definitions": definitions_schema,
    }
)

middleware: List[Middleware] = [
    Middleware(
        CORSMiddleware,
        allow_origins=[config["apostoAppURL"], config["apostoBetaURL"]],
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type", "Accept"],
    ),
]

with open("./doc/doc.yaml", "w") as doc_yaml:
    doc_yaml.write(yaml.dump(schemas.get_schema(routes)))

app: Starlette = Starlette(debug=True, middleware=middleware, routes=routes)
app.state.SEND_IN_BLUE_API_KEY = os.getenv("SEND_IN_BLUE_API_KEY")

for key in config.keys():
    setattr(app.state, key, config[key])

api_doc(app, config_path=Path("./doc/doc.yaml").as_posix(), url_prefix="/doc")
