import subprocess
import base64
import urllib.parse
from time import time
from datetime import datetime
import requests
from requests import Response
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import FileResponse, UJSONResponse
from starlette.status import HTTP_400_BAD_REQUEST
import ujson

with open("config.json", "r") as configData:
    config: dict = ujson.load(configData)

app: Starlette = Starlette(debug=True)

@app.route("/pdf/{receiptContentBase64}/{name}")
async def downloadReceipt(request: Request):
    receiptURL: str = f"{config['apostoAppURL']}/receipt/receipt.html?receiptContent={request.path_params['receiptContentBase64']}"

    subprocess.run(["npx", "electron-pdf", receiptURL, "out.pdf"])

    return FileResponse("out.pdf")

@app.route("/email/{receiptContentBase64}")
async def emailReceipt(request: Request):
    receiptContent: dict = ujson.decode(base64.b64decode(request.path_params["receiptContentBase64"]))
    receiptURL: str = urllib.parse.quote(f"{config['apostoAppURL']}/receipt/receipt.html?receiptContent={request.path_params['receiptContentBase64']}", safe='')
    receiptFilename: str = f"facture-{round(time())}.pdf"
    url: str = f"{config['apostoAPIURL']}/pdf/{receiptURL}/{receiptFilename}"

    data: str = ujson.encode({
        "sender": {
            "email": "facture@app.aposto.ch",
            "name": "Aposto"
        },
        "to": [{
            "email": receiptContent["customer"]["email"],
            "name": f"{receiptContent['customer']['firstName']} {receiptContent['customer']['lastName']}"
        }],
        "bcc": [{
            "email": receiptContent["author"]["email"],
            "name": receiptContent["author"]["name"]
        }],
        "htmlContent": f"<h1>Votre facture</h1><p>Bonjour {receiptContent['customer']['firstName']} {receiptContent['customer']['lastName']},</p><p>Vous pouvez dès à présent consulter votre facture du {datetime.now().strftime('%d/%m/%Y')} en pièce jointe.</p><p>À très bientôt,<br>{receiptContent['author']['name']}</p>",
        "subject": "Aposto - Votre nouvelle facture",
        "attachment": [{
            "url": url,
            "name": receiptFilename
        }]
    })

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": config["sendInBlueConfig"]["APIKey"]
    }
    
    response: Response = requests.request(
        "POST",
        f"{config['sendInBlueConfig']['APIURL']}/smtp/email",
        data=data,
        headers=headers
    )

    if response.status_code == 201:
        return UJSONResponse()
    else:
        responseContent: dict = ujson.decode(response.text)

        return UJSONResponse(responseContent, status_code=HTTP_400_BAD_REQUEST)