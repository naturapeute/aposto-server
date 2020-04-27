from pdf_generation.invoice_content import InvoiceContent
from tests.commons import InvoiceContentMissingParamTestCase, InvoiceContentTestCase


class InvoiceContentValidateTest(
    InvoiceContentTestCase, InvoiceContentMissingParamTestCase
):
    def setUp(self):
        InvoiceContentTestCase.setUp(self)
        InvoiceContentMissingParamTestCase.setUp(self)

    def test_validate_invoice_content(self):
        try:
            InvoiceContent.validate(self.invoice_content_dict)
        except ValueError:
            self.fail("InvoiceContent.validate raised ValueError unexpectedly!")

    def test_validate_invoice_content_missing_param(self):
        with self.assertRaises(ValueError) as context_manager:
            InvoiceContent.validate(self.invoice_content_missing_param_dict)

        self.assertDictEqual(
            context_manager.exception.args[0],
            InvoiceContentMissingParamTestCase.FAILURE_JSON,
        )


class InvoiceContentParseTest(InvoiceContentTestCase):
    def setUp(self):
        InvoiceContentTestCase.setUp(self)

    def test_parse_invoice_content(self):
        invoice_content: InvoiceContent = InvoiceContent(
            InvoiceContent.parse(self.invoice_content_base_64)
        )

        self.assertDictEqual(
            invoice_content._invoice_content_dict, self.invoice_content_dict
        )
