import base64
import os
from pathlib import Path
from typing import Dict, List

import requests
import ujson
from dotenv import load_dotenv
from requests import Response as RequestsResponse
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import (
    FileResponse,
    PlainTextResponse,
    RedirectResponse,
    UJSONResponse,
)
from starlette.status import HTTP_400_BAD_REQUEST

from pdf_generation.aposto_pdf import ApostoCanvas
from pdf_generation.invoice_content import InvoiceContent

load_dotenv()
SEND_IN_BLUE_API_KEY = os.getenv("SEND_IN_BLUE_API_KEY")

with open("config.json", "r") as configData:
    ENV = os.getenv("ENV")
    fullConfig: Dict[str, Dict[str, str]] = ujson.load(configData)
    config: Dict[str, str] = fullConfig["PROD"] if ENV == "PROD" else fullConfig["DEV"]

middleware: List[Middleware] = [
    Middleware(CORSMiddleware, allow_origins=[config["apostoAppURL"]])
]

app: Starlette = Starlette(debug=True, middleware=middleware)


@app.route("/pdf/{invoice_content_base_64}/{name}")
async def download_invoice(request: Request):
    invoice_path: Path = generate_invoice(
        parse_invoice_content(request.path_params["invoice_content_base_64"])
    )

    return FileResponse(invoice_path.as_posix())


@app.route("/email/{invoice_content_base_64}")
async def email_invoice(request: Request):
    invoice_content: InvoiceContent = parse_invoice_content(
        request.path_params["invoice_content_base_64"]
    )

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
            "attachment": [
                {"content": invoice_file_base_64, "name": invoice_path.name}
            ],
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
async def icon(request: Request):
    return RedirectResponse("https://terrapeute.ch/img/favicon.png")


@app.route("/gln", methods=["POST"])
async def gln(request: Request):
    body: Dict[str, str] = await request.json()

    if not "name" in body and not ("firstName" in body and "lastName" in body):
        return UJSONResponse(
            {"name": "Name or first name and last name parameters are missing."},
            status_code=HTTP_400_BAD_REQUEST,
        )

    form_body: List[str] = ["SearchRole=CompTherapist"]

    if "name" in body:
        form_body.append(f"SearchDescription={body['name']}")
    else:
        form_body.append(f"SearchDescription={body['lastName']}")
        form_body.append(f"SearchDescription2={body['firstName']}")

    if "ZIP" in body:
        form_body.append(f"SearchZip={body['ZIP']}")

    if "city" in body:
        form_body.append(f"SearchCity={body['city']}")

    url: str = f"https://refdatabase.refdata.ch/Viewer/SearchPartner{'Jur' if 'name' in body else 'Nat'}?Lang=fr"

    headers: Dict[str, str] = {
        "accept": "text/html",
        "content-type": "application/x-www-form-urlencoded",
    }

    response: RequestsResponse = requests.post(
        url, data="&".join(form_body), headers=headers
    )

    return PlainTextResponse(response.text)


def generate_invoice(invoice_content: InvoiceContent) -> Path:
    invoice_dir: Path = Path(
        f"./out/{invoice_content.author.name}/{invoice_content.author.RCC}"
    )
    invoice_dir.mkdir(parents=True, exist_ok=True)
    invoice_path: Path = invoice_dir.joinpath(
        f"invoice-{invoice_content.timestamp}.pdf"
    )

    if not invoice_path.exists():
        cvs: ApostoCanvas = ApostoCanvas(invoice_path.as_posix())

        cvs.draw_full_invoice(
            [
                Path(
                    "pdf_generation/templates/descriptor_templates/header_template.json"
                ),
                Path(
                    "pdf_generation/templates/descriptor_templates/author_template.json"
                ),
                Path(
                    "pdf_generation/templates/descriptor_templates/patient_template.json"
                ),
                Path(
                    "pdf_generation/templates/descriptor_templates/other_fields_template.json"
                ),
                Path(
                    "pdf_generation/templates/descriptor_templates/services_template.json"
                ),
                Path(
                    "pdf_generation/templates/descriptor_templates/footer_template.json"
                ),
            ],
            [Path("pdf_generation/templates/graphic_templates/frame_template.json")],
            [
                Path("pdf_generation/templates/value_templates/author_template.json"),
                Path("pdf_generation/templates/value_templates/patient_template.json"),
                Path(
                    "pdf_generation/templates/value_templates/other_fields_template.json"
                ),
                Path("pdf_generation/templates/value_templates/services_template.json"),
                Path("pdf_generation/templates/value_templates/footer_template.json"),
            ],
            invoice_content,
        )

        cvs.showPage()
        cvs.save()

    return invoice_path


def parse_invoice_content(invoice_content_base_64: str) -> InvoiceContent:
    return InvoiceContent(
        ujson.loads(base64.b64decode(invoice_content_base_64).decode("latin1"))
    )
