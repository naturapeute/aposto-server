import base64
from json.decoder import JSONDecodeError
from pathlib import Path
from typing import Dict

import requests
import ujson
from pydantic import ValidationError
from requests import Response as RequestsResponse
from starlette.requests import Request
from starlette.responses import UJSONResponse
from starlette.status import HTTP_400_BAD_REQUEST

from models import Invoice
from pdf_generation import PDFGenerator
from pdf_generation.contents import InvoiceContent


async def email_endpoint(request: Request):
    """
    summary: Send an invoice by email
    description: >
        Generate an invoice as PDF, based on Tarif 590 and QR-invoice Swiss standards and send it
        to the author's and patient's mail addresses

    requestBody:
        description: The content used to generate the PDF invoice
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
                            -   $ref: '#/components/schemas/JSONError'
                            -   type: array
                                items:
                                    $ref: '#/components/schemas/ValidationError'
                            -   $ref: '#/components/schemas/SendinBlueError'
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

    invoice_path: Path = PDFGenerator(invoice_content).generate_invoice()

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
        "api-key": request.app.state.SEND_IN_BLUE_API_KEY,
    }

    response: RequestsResponse = requests.post(
        f"{request.app.state.sendInBlueAPIURL}/smtp/email", data=data, headers=headers
    )

    if response.status_code == 201:
        return UJSONResponse()

    return UJSONResponse(ujson.loads(response.text), status_code=HTTP_400_BAD_REQUEST)
