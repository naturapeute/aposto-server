import subprocess
import base64
import urllib.parse
from time import time
from datetime import datetime
import requests
from requests import Response
from dotenv import load_dotenv
import os
from typing import List, Dict

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import FileResponse, UJSONResponse
from starlette.status import HTTP_400_BAD_REQUEST
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
import ujson

load_dotenv()
SEND_IN_BLUE_API_KEY = os.getenv("SEND_IN_BLUE_API_KEY")

with open("config.json", "r") as configData:
    config: Dict = ujson.load(configData)

middleware: List[Middleware] = [
    Middleware(CORSMiddleware, allow_origins=[config["apostoAppURL"]])
]

app: Starlette = Starlette(debug=True, middleware=middleware)


@app.route("/pdf/{receiptContentBase64}/{name}")
async def downloadReceipt(request: Request):
    generateReceipt(request.path_params["receiptContentBase64"])

    return FileResponse("out.pdf")


@app.route("/email/{receiptContentBase64}")
async def emailReceipt(request: Request):
    receipt_content: Dict = ujson.loads(
        base64.b64decode(request.path_params["receiptContentBase64"]).decode("latin1")
    )
    receipt_filename: str = f"facture-{round(time())}.pdf"

    generateReceipt(request.path_params["receiptContentBase64"])

    with open("out.pdf", "rb") as receiptFile:
        receiptFileBase64 = base64.b64encode(receiptFile.read())

    data: str = ujson.dumps(
        {
            "sender": {"email": "facture@app.aposto.ch", "name": "Aposto"},
            "to": [
                {
                    "email": receipt_content["customer"]["email"],
                    "name": f"{receipt_content['customer']['firstName']} {receipt_content['customer']['lastName']}",
                }
            ],
            "bcc": [
                {
                    "email": receipt_content["author"]["email"],
                    "name": receipt_content["author"]["name"],
                }
            ],
            "htmlContent": f"<h1>Votre facture</h1><p>Bonjour {receipt_content['customer']['firstName']} {receipt_content['customer']['lastName']},</p><p>Vous pouvez dès à présent consulter votre facture du {datetime.now().strftime('%d/%m/%Y')} en pièce jointe.</p><p>À très bientôt,<br>{receipt_content['author']['name']}</p>",
            "subject": "Aposto - Votre nouvelle facture",
            "attachment": [{"content": receiptFileBase64, "name": receipt_filename}],
        }
    )

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": SEND_IN_BLUE_API_KEY,
    }

    response: Response = requests.post(
        f"{config['sendInBlueAPIURL']}/smtp/email", data=data, headers=headers
    )

    if response.status_code == 201:
        return UJSONResponse()

    response_content: Dict = ujson.loads(response.text)

    return UJSONResponse(response_content, status_code=HTTP_400_BAD_REQUEST)


def generateReceipt(receiptContentBase64: str):
    receipt_url: str = f"https://app.aposto.ch/receipt/receipt.html?receiptContent={receiptContentBase64}"

    subprocess.Popen(f"npx electron-pdf {receipt_url} out.pdf", shell=True)
