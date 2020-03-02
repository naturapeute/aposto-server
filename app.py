import subprocess
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import FileResponse

app: Starlette = Starlette(debug=True)

@app.route("/pdf/{receiptContentBase64}/{name}")
async def downloadReceipt(request: Request):
    receiptURL: str = f"http://app.aposto.ch/receipt/receipt.html?receiptContent={request.path_params['receiptContentBase64']}"

    subprocess.run(['npx', 'electron-pdf', receiptURL, 'out.pdf'])

    return FileResponse('out.pdf')