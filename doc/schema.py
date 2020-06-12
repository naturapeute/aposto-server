from pathlib import Path

import yaml
from starlette.applications import Starlette
from starlette.schemas import SchemaGenerator
from swagger_ui import api_doc

from models import Invoice
from routes import routes


def generate_schema(app: Starlette):
    invoice_schema: dict = Invoice.schema()
    definitions_schema: dict = invoice_schema["definitions"]
    invoice_schema.pop("definitions", None)

    schema_generator: SchemaGenerator = SchemaGenerator(
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

    with open("./doc/doc.yaml", "w") as doc_yaml:
        doc_yaml.write(yaml.dump(schema_generator.get_schema(routes)))

    api_doc(app, config_path=Path("./doc/doc.yaml").as_posix(), url_prefix="/doc")
