from unittest import TestCase
import datetime
from pathlib import Path

import responses
from requests import Response
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from starlette.testclient import TestClient

from app import app
from tests.commons import InvoiceContentTestCase, SendInBlueMock


class APITestCase(TestCase):
    def setUp(self):
        self.test_client: TestClient = TestClient(app)


class PDFEndpointTest(APITestCase, InvoiceContentTestCase):
    def setUp(self):
        APITestCase.setUp(self)
        InvoiceContentTestCase.setUp(self)
        Path(
            f"./out/{self.invoice_content_dict['author']['name']}/{self.invoice_content_dict['author']['RCCNumber']}/invoice-{int(self.invoice_content_dict['timestamp'] / 1000)}.pdf"
        ).unlink()


    def test_pdf_endpoint(self):
        test_time: datetime.datetime = datetime.datetime.now()
        test_time_str: str = test_time.strftime("%Y%m%d%H%M%S")

        response: Response = self.test_client.get(
            f"/pdf/{self.invoice_content_base_64}/invoice.pdf"
        )

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.headers["Content-Type"], "application/pdf")
        self.assertTrue(f"/CreationDate (D:{test_time_str}" in response.text)


class EmailEndpointTest(APITestCase, InvoiceContentTestCase):
    def setUp(self):
        APITestCase.setUp(self)
        InvoiceContentTestCase.setUp(self)


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
        self.assertDictEqual(response.json(), SendInBlueMock.failure_json())
