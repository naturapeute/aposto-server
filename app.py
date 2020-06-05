import base64
import binascii
import os
import re
from pathlib import Path
from typing import Dict, List

import requests
import ujson
from dotenv import load_dotenv
from requests import Response as RequestsResponse
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import (
    FileResponse,
    RedirectResponse,
    Response,
    UJSONResponse,
)
from starlette.status import HTTP_400_BAD_REQUEST

from pdf_generation.aposto_pdf import ApostoCanvas
from pdf_generation.invoice_content import InvoiceContent


class InvoiceContentMiddleware(BaseHTTPMiddleware):
    INVOICE_CONTENT_ROUTES = [
        r"^/pdf/([^/]*)/.*$",
        r"^/email/([^/]*)$",
    ]

    async def dispatch(self, request: Request, call_next) -> Response:
        invoice_content_base_64: str = ""
        error_message: Dict = {}

        for invoice_content_route in self.INVOICE_CONTENT_ROUTES:
            match = re.search(invoice_content_route, request.url.path)

            if match:
                invoice_content_base_64 = match.group(1)
                break

        if invoice_content_base_64:
            invoice_content_dict = {}

            try:
                invoice_content_dict: Dict = InvoiceContent.parse(invoice_content_base_64)

                try:
                    InvoiceContent.validate(invoice_content_dict)

                    request.state.invoice_content: InvoiceContent = InvoiceContent(
                        invoice_content_dict
                    )
                except ValueError as missing_params:
                    error_message = missing_params.args[0]
            except binascii.Error:
                error_message = {"error": "Improper base64 provided"}
            except ValueError:
                error_message = {"error": "Improper JSON provided inside base64"}

            request.state.error_message: Dict = error_message

        return await call_next(request)


load_dotenv()
SEND_IN_BLUE_API_KEY = os.getenv("SEND_IN_BLUE_API_KEY")

with open("config.json", "r") as configData:
    ENV = os.getenv("ENV")
    fullConfig: Dict[str, Dict[str, str]] = ujson.load(configData)
    config: Dict[str, str] = fullConfig["PROD"] if ENV == "PROD" else fullConfig["DEV"]

middleware: List[Middleware] = [
    Middleware(InvoiceContentMiddleware),
    Middleware(
        CORSMiddleware,
        allow_origins=[config["apostoAppURL"], config["apostoBetaURL"]],
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type", "Accept"],
    ),
]

app: Starlette = Starlette(debug=True, middleware=middleware)


@app.route("/pdf/{invoice_content_base_64}/{name}")
async def download_invoice(request: Request):
    invoice_content: InvoiceContent = None

    try:
        invoice_content = request.state.invoice_content
    except AttributeError:
        return UJSONResponse(request.state.error_message, HTTP_400_BAD_REQUEST)

    invoice_path: Path = generate_invoice(invoice_content)

    return FileResponse(invoice_path.as_posix())


@app.route("/email/{invoice_content_base_64}")
async def email_invoice(request: Request):
    invoice_content: InvoiceContent = None

    try:
        invoice_content = request.state.invoice_content
    except AttributeError:
        return UJSONResponse(request.state.error_message, HTTP_400_BAD_REQUEST)

    invoice_path: Path = generate_invoice(invoice_content)

    with open(invoice_path.as_posix(), "rb") as invoice_file:
        invoice_file_base_64 = base64.b64encode(invoice_file.read())

    data: str = ujson.dumps(
        {
            "sender": {"email": "facture@app.aposto.ch", "name": "Aposto"},
            "to": [
                {
                    "email": invoice_content.patient.email,
                    "name": f"{invoice_content.patient.first_name} {invoice_content.patient.last_name}",
                }
            ],
            "bcc": [
                {
                    "email": invoice_content.author.email,
                    "name": invoice_content.author.name,
                }
            ],
            "htmlContent": f"<h1>Votre facture</h1><p>Bonjour {invoice_content.patient.first_name} {invoice_content.patient.last_name},</p><p>Vous pouvez dès à présent consulter votre facture du {invoice_content.date_string} en pièce jointe.</p><p>À très bientôt,<br>{invoice_content.author.name}</p>",
            "subject": "Aposto - Votre nouvelle facture",
            "attachment": [{"content": invoice_file_base_64, "name": invoice_path.name}],
        }
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

    response_content: Dict[str, str] = ujson.loads(response.text)

    return UJSONResponse(response_content, status_code=HTTP_400_BAD_REQUEST)


@app.route("/favicon.ico")
async def icon(_: Request):
    return RedirectResponse("https://naturapeute.ch/img/favicon.png")


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
