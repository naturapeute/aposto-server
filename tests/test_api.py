from datetime import datetime
from pathlib import Path
from unittest import TestCase

import responses
from requests import Response
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from starlette.testclient import TestClient

from app import app
from models.invoice import Invoice
from tests.commons import (
    InvoiceContentDemoModeTestCase,
    InvoiceContentImproperJSONTestCase,
    InvoiceContentInvalidTestCase,
    InvoiceContentTestCase,
    SendInBlueMock,
)


class APITestCase(TestCase):
    def setUp(self):
        self.test_client: TestClient = TestClient(app)


class PDFEndpointTest(
    APITestCase,
    InvoiceContentTestCase,
    InvoiceContentDemoModeTestCase,
    InvoiceContentInvalidTestCase,
    InvoiceContentImproperJSONTestCase,
):
    def setUp(self):
        APITestCase.setUp(self)
        InvoiceContentTestCase.setUp(self)
        InvoiceContentDemoModeTestCase.setUp(self)
        InvoiceContentInvalidTestCase.setUp(self)
        InvoiceContentImproperJSONTestCase.setUp(self)

        invoice: Invoice = Invoice.parse_raw(self.invoice_json)

        self.invoice_path: Path = Path(
            f"./out/{invoice.naturapeuteID}/invoice-{int(datetime.timestamp(invoice.timestamp))}.pdf"
        )

        if self.invoice_path.is_file():
            self.invoice_path.unlink()

        self.invoice_path_demo: Path = Path(
            f"./out/demo/invoice-{int(datetime.timestamp(invoice.timestamp))}.pdf"
        )

        if self.invoice_path_demo.is_file():
            self.invoice_path_demo.unlink()

    def test_pdf_endpoint(self):
        test_time: datetime = datetime.now()
        test_time_str: str = test_time.strftime("%Y%m%d%H%M%S")

        response: Response = self.test_client.post(
            f"/pdf/invoice.pdf", json=self.invoice_json
        )

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.headers["Content-Type"], "application/pdf")
        self.assertTrue(f"/CreationDate (D:{test_time_str}" in response.text)
        self.assertTrue(self.invoice_path.is_file())

    def test_pdf_endpoint_demo_mode(self):
        test_time: datetime = datetime.now()
        test_time_str: str = test_time.strftime("%Y%m%d%H%M%S")

        response: Response = self.test_client.post(
            f"/pdf/invoice.pdf", json=self.invoice_demo_json
        )

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.headers["Content-Type"], "application/pdf")
        self.assertTrue(f"/CreationDate (D:{test_time_str}" in response.text)
        self.assertTrue(self.invoice_path_demo.is_file())

    def test_pdf_endpoint_invalid_content(self):
        response: Response = self.test_client.post(
            f"/pdf/invoice.pdf", json=self.invoice_invalid_json
        )

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), InvoiceContentInvalidTestCase.FAILURE_JSON)

    def test_pdf_endpoint_improper_json(self):
        response: Response = self.test_client.post(
            f"/pdf/invoice.pdf", json=self.invoice_improper_json
        )

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), InvoiceContentImproperJSONTestCase.FAILURE_JSON)


class EmailEndpointTest(
    APITestCase,
    InvoiceContentTestCase,
    InvoiceContentInvalidTestCase,
    InvoiceContentImproperJSONTestCase,
):
    def setUp(self):
        APITestCase.setUp(self)
        InvoiceContentTestCase.setUp(self)
        InvoiceContentInvalidTestCase.setUp(self)
        InvoiceContentImproperJSONTestCase.setUp(self)

    @responses.activate
    def test_email_endpoint_success(self):
        responses.add(SendInBlueMock.smtp_email_success_request())

        response: Response = self.test_client.post(f"/email", json=self.invoice_json)

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.headers["Content-Type"], "application/json")

    @responses.activate
    def test_email_endpoint_failure(self):
        responses.add(SendInBlueMock.smtp_email_failure_request())

        response: Response = self.test_client.post(f"/email", json=self.invoice_json)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertDictEqual(response.json(), SendInBlueMock.FAILURE_JSON)

    def test_email_endpoint_invalid_content(self):
        response: Response = self.test_client.post(
            f"/email", json=self.invoice_invalid_json
        )

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), InvoiceContentInvalidTestCase.FAILURE_JSON)

    def test_email_endpoint_improper_json(self):
        response: Response = self.test_client.post(
            f"/email", json=self.invoice_improper_json
        )

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), InvoiceContentImproperJSONTestCase.FAILURE_JSON)
