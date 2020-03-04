import subprocess
import base64
import urllib.parse
from time import time
from datetime import datetime
import requests
from dotenv import load_dotenv
import os
from typing import List, Dict

from requests import Response
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
    Middleware(CORSMiddleware, allow_origins=["https://app.aposto.ch/"])
]

app: Starlette = Starlette(debug=True, middleware=middleware)


@app.route("/pdf/{receiptContentBase64}/{name}")
async def downloadReceipt(request: Request):
    receipt_url: str = f"{config['apostoAppURL']}/receipt/receipt.html?receiptContent={request.path_params['receiptContentBase64']}"

    subprocess.call(["npx", "electron-pdf", receipt_url, "out.pdf"])

    return FileResponse("out.pdf")


@app.route("/email/{receiptContentBase64}")
async def emailReceipt(request: Request):
    receipt_content: Dict = ujson.loads(
        base64.b64decode(request.path_params["receiptContentBase64"])
    )
    receipt_url: str = urllib.parse.quote(
        f"{config['apostoAppURL']}/receipt/receipt.html?receiptContent={request.path_params['receiptContentBase64']}",
        safe="",
    )
    receipt_filename: str = f"facture-{round(time())}.pdf"
    url: str = f"{config['apostoAPIURL']}/pdf/{receipt_url}/{receipt_filename}"

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
            "attachment": [{"url": url, "name": receipt_filename}],
        }
    )

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": SEND_IN_BLUE_API_KEY,
    }

    response: Response = requests.request(
        "POST", f"{config['sendInBlueAPIURL']}/smtp/email", data=data, headers=headers,
    )

    if response.status_code == 201:
        return UJSONResponse()
    else:
        response_content: Dict = ujson.loads(response.text)

        return UJSONResponse(response_content, status_code=HTTP_400_BAD_REQUEST)
