import base64
import os
from json.decoder import JSONDecodeError
from pathlib import Path
from typing import Dict, List

import requests
import ujson
from dotenv import load_dotenv
from pydantic import ValidationError
from requests import Response as RequestsResponse
from spectree import Response, SpecTree
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import FileResponse, RedirectResponse, UJSONResponse
from starlette.status import HTTP_400_BAD_REQUEST

from models.invoice import Invoice
from pdf_generation.aposto_pdf import ApostoCanvas
from pdf_generation.contents.invoice_content import InvoiceContent

load_dotenv()
SEND_IN_BLUE_API_KEY = os.getenv("SEND_IN_BLUE_API_KEY")

with open("config.json", "r") as configData:
    ENV = os.getenv("ENV")
    fullConfig: Dict[str, Dict[str, str]] = ujson.load(configData)
    config: Dict[str, str] = fullConfig["PROD"] if ENV == "PROD" else fullConfig["DEV"]

api: SpecTree = SpecTree("starlette")

middleware: List[Middleware] = [
    Middleware(
        CORSMiddleware,
        allow_origins=[config["apostoAppURL"], config["apostoBetaURL"]],
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type", "Accept"],
    ),
]

app: Starlette = Starlette(debug=True, middleware=middleware)
api.register(app)


@api.validate(json=Invoice, tags=["api"])
@app.route("/pdf/{name}", methods=["POST"])
async def download_invoice(request: Request):
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


@api.validate(json=Invoice, resp=Response(HTTP_201=None, HTTP_400=None), tags=["api"])
@app.route("/email", methods=["POST"])
async def email_invoice(request: Request):
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

    return UJSONResponse(ujson.loads(response.text), status_code=HTTP_400_BAD_REQUEST)


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
