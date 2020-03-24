from app import parse_invoice_content
from pdf_generation.invoice_content import InvoiceContent
from tests.commons import InvoiceContentTestCase


class UtilsTest(InvoiceContentTestCase):
    def test_parse_invoice_content(self):
        invoice_content: InvoiceContent = parse_invoice_content(
            self.invoice_content_base_64
        )

        self.assertDictEqual(
            invoice_content._invoice_content_dict, self.invoice_content_dict
        )
