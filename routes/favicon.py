from starlette.requests import Request
from starlette.responses import RedirectResponse


async def favicon_endpoint(_: Request):
    return RedirectResponse("https://naturapeute.ch/img/favicon.png")
