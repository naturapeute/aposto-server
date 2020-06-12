import base64
import os
from json.decoder import JSONDecodeError
from pathlib import Path
from typing import Dict, List

import requests
import ujson
import yaml
from dotenv import load_dotenv
from pydantic import ValidationError
from requests import Response as RequestsResponse
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import FileResponse, RedirectResponse, UJSONResponse
from starlette.schemas import SchemaGenerator
from starlette.status import HTTP_400_BAD_REQUEST
from swagger_ui import api_doc

from models.invoice import Invoice
from pdf_generation.aposto_pdf import ApostoCanvas
from pdf_generation.contents.invoice_content import InvoiceContent

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
                "JSON Error": {
                    "description": "An error occurring when the request body contains wrongly formatted JSON",
                    "properties": {
                        "json_error": {
                            "description": "An error message describing the JSON error. The syntax error position is provided",
                            "type": "string",
                        }
                    },
                },
                "Validation Error": {
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
                "SendinBlue Error": {
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

app: Starlette = Starlette(debug=True, middleware=middleware)


@app.route("/pdf/{name}", methods=["POST"])
async def download_invoice(request: Request):
    """
    summary: Generate an invoice as PDF
    description: Generate an invoice as PDF, based on Tarif 590 and QR-invoice standards

    parameters:
        -   in: path
            name: name
            schema:
                type: string
            required: true
            description: The generated PDF invoice filename. It is needed when downloading the PDF from this endpoint or when opening the PDF in a browser directly from the endpoint URL. It should end with _.pdf_

    requestBody:
        summary: The content used to generate the PDF invoice
        required: true
        content:
            application/json:
                schema:
                    $ref: '#/components/schemas/Invoice'

    responses:
        200:
            description: The generated PDF invoice
            content:
                application/pdf:
                    schema:
                        type: string
                        format: binary
        400:
            description: Bad Request Error
            content:
                application/json:
                    schema:
                        oneOf:
                            -   $ref: '#/components/schemas/JSON Error'
                            -   type: array
                                items:
                                    $ref: '#/components/schemas/Validation Error'
    """

    try:
        invoice_dict: dict = await request.json()
    except JSONDecodeError as json_error:
        error_msg: str = f"{json_error.msg}: line {json_error.lineno} column {json_error.colno} (char {json_error.pos})"

        return UJSONResponse({"json_error": error_msg}, status_code=HTTP_400_BAD_REQUEST)

    try:
        invoice: Invoice = Invoice(**invoice_dict)
    except ValidationError as validation_error:
        return UJSONResponse(validation_error.errors(), status_code=HTTP_400_BAD_REQUEST)

    invoice_content: InvoiceContent = InvoiceContent(invoice)

    invoice_path: Path = generate_invoice(invoice_content)

    return FileResponse(invoice_path.as_posix())


@app.route("/email", methods=["POST"])
async def email_invoice(request: Request):
    """
    summary: Send an invoice
    description: Generate an invoice as PDF, based on Tarif 590 and QR-invoice standards and send it to the author's and patient's mail addresses

    requestBody:
        summary: The content used to generate the PDF invoice
        required: true
        content:
            application/json:
                schema:
                    $ref: '#/components/schemas/Invoice'

    responses:
        201:
            description: The invoice as been successfully sent
        400:
            description: Bad Request Error
            content:
                application/json:
                    schema:
                        oneOf:
                            -   $ref: '#/components/schemas/JSON Error'
                            -   type: array
                                items:
                                    $ref: '#/components/schemas/Validation Error'
                            -   $ref: '#/components/schemas/SendinBlue Error'
    """

    try:
        invoice_dict: dict = await request.json()
    except JSONDecodeError as json_error:
        error_msg: str = f"{json_error.msg}: line {json_error.lineno} column {json_error.colno} (char {json_error.pos})"

        return UJSONResponse({"json_error": error_msg}, status_code=HTTP_400_BAD_REQUEST)

    try:
        invoice: Invoice = Invoice(**invoice_dict)
    except ValidationError as validation_error:
        return UJSONResponse(validation_error.errors(), status_code=HTTP_400_BAD_REQUEST)

    invoice_content: InvoiceContent = InvoiceContent(invoice)

    invoice_path: Path = generate_invoice(invoice_content)

    with open(invoice_path.as_posix(), "rb") as invoice_file:
        invoice_file_base_64 = base64.b64encode(invoice_file.read())

    data: str = ujson.dumps(
        {
            "sender": {"email": "facture@app.aposto.ch", "name": "Aposto"},
            "to": [
                {
                    "email": invoice.patient.email,
                    "name": f"{invoice.patient.firstName} {invoice.patient.lastName}",
                }
            ],
            "bcc": [{"email": invoice.author.email, "name": invoice.author.name,}],
            "htmlContent": f"<h1>Votre facture</h1><p>Bonjour {invoice.patient.firstName} {invoice.patient.lastName},</p><p>Vous pouvez dès à présent consulter votre facture du {invoice_content.date_string} en pièce jointe.</p><p>À très bientôt,<br>{invoice.author.name}</p>",
            "subject": "Aposto - Votre nouvelle facture",
            "attachment": [{"content": invoice_file_base_64, "name": invoice_path.name}],
        },
        reject_bytes=False,
    )

    headers: Dict[str, str] = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": SEND_IN_BLUE_API_KEY,
    }

    response: RequestsResponse = requests.post(
        f"{config['sendInBlueAPIURL']}/smtp/email", data=data, headers=headers
    )

    if response.status_code == 201:
        return UJSONResponse()

    return UJSONResponse(ujson.loads(response.text), status_code=HTTP_400_BAD_REQUEST)


@app.route("/favicon.ico", include_in_schema=False)
async def icon(_: Request):
    return RedirectResponse("https://naturapeute.ch/img/favicon.png")


# NOTE : The schema generation is done after routes are defined so they are registered in the server
with open("./doc/doc.yaml", "w") as doc_yaml:
    doc_yaml.write(yaml.dump(schemas.get_schema(app.routes)))

api_doc(app, config_path=Path("./doc/doc.yaml").as_posix(), url_prefix="/doc")


def generate_invoice(invoice_content: InvoiceContent) -> Path:
    invoice_dir_str = (
        f"./out/{invoice_content.naturapeute_id}"
        if invoice_content.naturapeute_id
        else "./out/demo"
    )
    invoice_dir: Path = Path(invoice_dir_str)
    invoice_dir.mkdir(parents=True, exist_ok=True)
    invoice_path: Path = invoice_dir.joinpath(f"invoice-{invoice_content.timestamp}.pdf")

    if not invoice_path.exists():
        cvs: ApostoCanvas = ApostoCanvas(invoice_path.as_posix())

        cvs.draw_invoice(
            [
                Path(
                    "pdf_generation/qr_invoice_templates/descriptor_templates/header_template.json"
                ),
                Path(
                    "pdf_generation/qr_invoice_templates/descriptor_templates/author_template.json"
                ),
                Path(
                    "pdf_generation/qr_invoice_templates/descriptor_templates/patient_template.json"
                ),
                Path(
                    "pdf_generation/qr_invoice_templates/descriptor_templates/invoice_template.json"
                ),
            ],
            [
                Path(
                    "pdf_generation/qr_invoice_templates/graphic_templates/invoice_frame_template.json"
                )
            ],
            [
                Path(
                    "pdf_generation/qr_invoice_templates/value_templates/author_template.json"
                ),
                Path(
                    "pdf_generation/qr_invoice_templates/value_templates/patient_template.json"
                ),
                Path(
                    "pdf_generation/qr_invoice_templates/value_templates/invoice_template.json"
                ),
            ],
            [],
            invoice_content,
        )

        if invoice_content.qr_reference and invoice_content.author.qr_iban:
            cvs.draw_descriptor_template(
                Path(
                    "pdf_generation/qr_invoice_templates/descriptor_templates/receipt_template.json"
                )
            )
            cvs.draw_descriptor_template(
                Path(
                    "pdf_generation/qr_invoice_templates/descriptor_templates/payment_section_template.json"
                )
            )

            cvs.draw_value_template(
                Path(
                    "pdf_generation/qr_invoice_templates/value_templates/receipt_template.json"
                ),
                invoice_content,
            )
            cvs.draw_value_template(
                Path(
                    "pdf_generation/qr_invoice_templates/value_templates/payment_section_template.json"
                ),
                invoice_content,
            )

            cvs.draw_frame_template(
                Path(
                    "pdf_generation/qr_invoice_templates/graphic_templates/qr_invoice_frame_template.json"
                )
            )

            cvs.draw_scissors_template(
                Path(
                    "pdf_generation/qr_invoice_templates/graphic_templates/scissors_template.json"
                )
            )

            cvs.draw_swiss_qr_code_template(
                Path(
                    "pdf_generation/qr_invoice_templates/graphic_templates/swiss_qr_code_template.json"
                ),
                invoice_content,
            )

        cvs.showPage()

        cvs.draw_invoice(
            [
                Path(
                    "pdf_generation/invoice_templates/descriptor_templates/header_template.json"
                ),
                Path(
                    "pdf_generation/invoice_templates/descriptor_templates/author_template.json"
                ),
                Path(
                    "pdf_generation/invoice_templates/descriptor_templates/patient_template.json"
                ),
                Path(
                    "pdf_generation/invoice_templates/descriptor_templates/other_fields_template.json"
                ),
                Path(
                    "pdf_generation/invoice_templates/descriptor_templates/services_template.json"
                ),
                Path(
                    "pdf_generation/invoice_templates/descriptor_templates/footer_template.json"
                ),
            ],
            [
                Path(
                    "pdf_generation/invoice_templates/graphic_templates/frame_template.json"
                )
            ],
            [
                Path(
                    "pdf_generation/invoice_templates/value_templates/author_template.json"
                ),
                Path(
                    "pdf_generation/invoice_templates/value_templates/patient_template.json"
                ),
                Path(
                    "pdf_generation/invoice_templates/value_templates/other_fields_template.json"
                ),
                Path(
                    "pdf_generation/invoice_templates/value_templates/services_template.json"
                ),
                Path(
                    "pdf_generation/invoice_templates/value_templates/footer_template.json"
                ),
            ],
            [
                Path(
                    "pdf_generation/invoice_templates/graphic_templates/datamatrix_template.json"
                ),
            ],
            invoice_content,
        )

        cvs.showPage()

        cvs.save()

    return invoice_path
