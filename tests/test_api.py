from unittest import TestCase

import responses
from requests import Response
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from starlette.testclient import TestClient

from app import app
from tests.commons import InvoiceContentTestCase, SendInBlueMock


class APITestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.test_client: TestClient = TestClient(app)


class PDFEndpointTest(APITestCase, InvoiceContentTestCase):
    def test_pdf_endpoint(self):
        response: Response = self.test_client.get(
            f"/pdf/{self.invoice_content_base_64}/invoice.pdf"
        )

        self.assertEqual(response.status_code, HTTP_200_OK)


class EmailEndpointTest(APITestCase, InvoiceContentTestCase):
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
