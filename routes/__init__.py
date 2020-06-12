from typing import List

from starlette.routing import Route

from .email import email_endpoint
from .favicon import favicon_endpoint
from .pdf import pdf_endpoint

routes: List[Route] = [
    Route("/favicon.ico", endpoint=favicon_endpoint, include_in_schema=False),
    Route("/pdf/{name}", endpoint=pdf_endpoint, methods=["POST"]),
    Route("/email", endpoint=email_endpoint, methods=["POST"]),
]
