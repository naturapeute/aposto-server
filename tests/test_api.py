import datetime
from pathlib import Path
from unittest import TestCase

import responses
from requests import Response
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from starlette.testclient import TestClient

from app import app
from tests.commons import (
    InvoiceContentImproperBase64TestCase,
    InvoiceContentImproperJSONTestCase,
    InvoiceContentTestCase,
    SendInBlueMock,
)


class APITestCase(TestCase):
    def setUp(self):
        self.test_client: TestClient = TestClient(app)


class PDFEndpointTest(
    APITestCase,
    InvoiceContentTestCase,
    InvoiceContentImproperBase64TestCase,
    InvoiceContentImproperJSONTestCase,
):
    def setUp(self):
        APITestCase.setUp(self)
        InvoiceContentTestCase.setUp(self)
        InvoiceContentImproperBase64TestCase.setUp(self)
        InvoiceContentImproperJSONTestCase.setUp(self)

        invoice_path: Path = Path(
            f"./out/{self.invoice_content_dict['author']['name']}/{self.invoice_content_dict['author']['RCC']}/invoice-{int(self.invoice_content_dict['timestamp'] / 1000)}.pdf"
        )

        if invoice_path.is_file():
            invoice_path.unlink()

    def test_pdf_endpoint(self):
        test_time: datetime.datetime = datetime.datetime.now()
        test_time_str: str = test_time.strftime("%Y%m%d%H%M%S")

        response: Response = self.test_client.get(
            f"/pdf/{self.invoice_content_base_64}/invoice.pdf"
        )

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.headers["Content-Type"], "application/pdf")
        self.assertTrue(f"/CreationDate (D:{test_time_str}" in response.text)

    def test_pdf_endpoint_improper_base(self):
        response: Response = self.test_client.get(
            f"/pdf/{self.invoice_content_improper_base_base_64}/invoice.pdf"
        )

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(), InvoiceContentImproperBase64TestCase.FAILURE_JSON
        )

    def test_pdf_endpoint_improper_json(self):
        response: Response = self.test_client.get(
            f"/pdf/{self.invoice_content_improper_json_base_64}/invoice.pdf"
        )

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(), InvoiceContentImproperJSONTestCase.FAILURE_JSON
        )


class EmailEndpointTest(
    APITestCase,
    InvoiceContentTestCase,
    InvoiceContentImproperBase64TestCase,
    InvoiceContentImproperJSONTestCase,
):
    def setUp(self):
        APITestCase.setUp(self)
        InvoiceContentTestCase.setUp(self)
        InvoiceContentImproperBase64TestCase.setUp(self)
        InvoiceContentImproperJSONTestCase.setUp(self)

    @responses.activate
    def test_email_endpoint_success(self):
        responses.add(SendInBlueMock.smtp_email_success_request())

        response: Response = self.test_client.get(
            f"/email/{self.invoice_content_base_64}"
        )

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.headers["Content-Type"], "application/json")

    @responses.activate
    def test_email_endpoint_failure(self):
        responses.add(SendInBlueMock.smtp_email_failure_request())

        response: Response = self.test_client.get(
            f"/email/{self.invoice_content_base_64}"
        )

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertDictEqual(response.json(), SendInBlueMock.FAILURE_JSON)

    def test_email_endpoint_improper_base(self):
        response: Response = self.test_client.get(
            f"/pdf/{self.invoice_content_improper_base_base_64}/invoice.pdf"
        )

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(), InvoiceContentImproperBase64TestCase.FAILURE_JSON
        )

    def test_email_endpoint_improper_json(self):
        response: Response = self.test_client.get(
            f"/pdf/{self.invoice_content_improper_json_base_64}/invoice.pdf"
        )

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(), InvoiceContentImproperJSONTestCase.FAILURE_JSON
        )
