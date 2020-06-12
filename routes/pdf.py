from json.decoder import JSONDecodeError
from pathlib import Path

from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import FileResponse, UJSONResponse
from starlette.status import HTTP_400_BAD_REQUEST

from models import Invoice
from pdf_generation import PDFGenerator
from pdf_generation.contents import InvoiceContent


async def pdf_endpoint(request: Request):
    """
    summary: Generate an invoice as PDF
    description: Generate an invoice as PDF, based on Tarif 590 and QR-invoice Swiss standards

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

    invoice_path: Path = PDFGenerator(invoice_content).generate_invoice()

    return FileResponse(invoice_path.as_posix())
