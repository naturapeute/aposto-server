from datetime import datetime, timezone
from unittest import TestCase

from pydantic import ValidationError

from models import Invoice


class InvoiceTestCase(TestCase):
    def setUp(self):
        self.invoice_dict: dict = {
            "naturapeuteID": "abcdef1234567890abcdef12",
            "author": {
                "name": "Cabinet de Leroy",
                "street": "Via delle Vigne 1",
                "ZIP": "7149",
                "city": "Vrin",
                "email": "LeroyFrechette@armyspy.com",
                "phone": "081 660 68 36",
                "RCC": "V123123",
            },
            "therapist": {
                "firstName": "Leroy",
                "lastName": "Fréchette",
                "street": "Via delle Vigne 1",
                "ZIP": "7149",
                "city": "Vrin",
                "email": "LeroyFrechette@armyspy.com",
                "phone": "081 660 68 36",
                "RCC": "V123123",
            },
            "patient": {
                "firstName": "Nicholas",
                "lastName": "Ailleboust",
                "street": "Tösstalstrasse 97",
                "ZIP": "8872",
                "city": "Weesen",
                "canton": "SG",
                "birthday": -1118102400.000,
                "gender": "female",
                "email": "NicholasAilleboust@teleworm.us",
            },
            "servicePrice": 100,
            "services": [
                {"date": 1584921600000, "code": 1003, "duration": 60},
                {"date": 1585008000000, "code": 1004, "duration": 30},
            ],
            "timestamp": 1585049118.485,
            "paid": True,
        }

    def test_valid(self):
        try:
            Invoice(**self.invoice_dict)
        except ValidationError:
            self.fail("Invoice is invalid while it should not.")

        self.invoice_dict["timestamp"] = 1585049118485

        try:
            Invoice(**self.invoice_dict)
        except ValidationError:
            self.fail("Invoice is invalid while it should not.")

        # FIXME : pydantic actually does not support JavaScript negative timestamp
        #           Enable this code when it will be properly parsed.
        #           See https://github.com/samuelcolvin/pydantic/issues/1600
        # self.invoice_dict["timestamp"] = -1585049118485

        # try:
        #     Invoice(**self.invoice_dict)
        # except ValidationError:
        #     self.fail("Invoice is invalid while it should not.")

    def test_valid_without_naturapeute_id(self):
        self.invoice_dict.pop("naturapeuteID")

        try:
            Invoice(**self.invoice_dict)
        except ValidationError:
            self.fail("Invoice is invalid while it should not.")

    def test_total_amount(self):
        invoice: Invoice = Invoice(**self.invoice_dict)

        self.assertEqual(invoice.total_amount, 150)

    def test_therapy_dates(self):
        invoice: Invoice = Invoice(**self.invoice_dict)
        (therapy_start_date, therapy_end_date) = invoice.therapy_dates

        self.assertEqual(datetime.timestamp(therapy_start_date), 1584921600.000)
        self.assertEqual(datetime.timestamp(therapy_end_date), 1585008000.000)

    def test_empty(self):
        with self.assertRaises(ValidationError):
            Invoice(**{})

    def test_wrong_naturapeute_id(self):
        self.invoice_dict["naturapeuteID"] = "abcdef1234567890abcdef1"

        with self.assertRaises(ValidationError):
            Invoice(**self.invoice_dict)

        self.invoice_dict["naturapeuteID"] = "abcdef1234567890abcdef123"

        with self.assertRaises(ValidationError):
            Invoice(**self.invoice_dict)

        self.invoice_dict["naturapeuteID"] = "abcdef1234567890abcdef1_"

        with self.assertRaises(ValidationError):
            Invoice(**self.invoice_dict)

    def test_missing_author(self):
        self.invoice_dict.pop("author")

        with self.assertRaises(ValidationError):
            Invoice(**self.invoice_dict)

    def test_wrong_author(self):
        self.invoice_dict["author"].pop("name")

        with self.assertRaises(ValidationError):
            Invoice(**self.invoice_dict)

    def test_missing_therapist(self):
        self.invoice_dict.pop("therapist")

        with self.assertRaises(ValidationError):
            Invoice(**self.invoice_dict)

    def test_wrong_therapist(self):
        self.invoice_dict["therapist"].pop("firstName")

        with self.assertRaises(ValidationError):
            Invoice(**self.invoice_dict)

    def test_missing_patient(self):
        self.invoice_dict.pop("patient")

        with self.assertRaises(ValidationError):
            Invoice(**self.invoice_dict)

    def test_wrong_patient(self):
        self.invoice_dict["patient"].pop("firstName")

        with self.assertRaises(ValidationError):
            Invoice(**self.invoice_dict)

    def test_missing_service_price(self):
        self.invoice_dict.pop("servicePrice")

        with self.assertRaises(ValidationError):
            Invoice(**self.invoice_dict)

    def test_wrong_service_price(self):
        self.invoice_dict["servicePrice"] = 0

        with self.assertRaises(ValidationError):
            Invoice(**self.invoice_dict)

    def test_missing_services(self):
        self.invoice_dict.pop("services")

        with self.assertRaises(ValidationError):
            Invoice(**self.invoice_dict)

    def test_wrong_services(self):
        self.invoice_dict["services"] = []

        with self.assertRaises(ValidationError):
            Invoice(**self.invoice_dict)

        self.invoice_dict["services"] = [1, 2]

        with self.assertRaises(ValidationError):
            Invoice(**self.invoice_dict)

        self.invoice_dict["services"] = [{"code": 1003, "duration": 60}]

        with self.assertRaises(ValidationError):
            Invoice(**self.invoice_dict)

        self.invoice_dict["services"] = [
            {"date": 1584921600000, "code": 1003, "duration": 60},
            {"date": 1584921600000, "code": 1003, "duration": 60},
            {"date": 1584921600000, "code": 1003, "duration": 60},
            {"date": 1584921600000, "code": 1003, "duration": 60},
            {"date": 1584921600000, "code": 1003, "duration": 60},
            {"date": 1584921600000, "code": 1003, "duration": 60},
        ]

        with self.assertRaises(ValidationError):
            Invoice(**self.invoice_dict)

    def test_timestamp_is_utc(self):
        invoice: Invoice = Invoice(**self.invoice_dict)

        self.assertEqual(invoice.timestamp.tzinfo, timezone.utc)

    def test_missing_timestamp(self):
        self.invoice_dict.pop("timestamp")

        with self.assertRaises(ValidationError):
            Invoice(**self.invoice_dict)

        # FIXME : pydantic actually does not support JavaScript negative timestamp
        #           Remove this code when it will be properly parsed.
        #           See https://github.com/samuelcolvin/pydantic/issues/1600
        self.invoice_dict["timestamp"] = -1585049118485

        with self.assertRaises(ValidationError):
            Invoice(**self.invoice_dict)

    def test_wrong_timestamp(self):
        self.invoice_dict["timestamp"] = "test"

        with self.assertRaises(ValidationError):
            Invoice(**self.invoice_dict)

    def test_empty_reference(self):
        invoice: Invoice = Invoice(**self.invoice_dict)

        self.assertEqual(invoice.reference_type, "NON")
        self.assertIsNone(invoice.reference)

    def test_creditor_reference(self):
        self.invoice_dict["author"]["IBAN"] = "CH2641234567890123456"

        invoice: Invoice = Invoice(**self.invoice_dict)

        self.assertEqual(invoice.reference_type, "SCOR")
        self.assertTrue(invoice.reference.startswith("RF"))
        self.assertEqual(
            int(f"{invoice.reference[4:]}2715{invoice.reference[2:4]}") % 97, 1
        )

    def test_qr_reference(self):
        self.invoice_dict["author"]["IBAN"] = "CH5131234567890123456"

        invoice: Invoice = Invoice(**self.invoice_dict)

        self.assertEqual(invoice.reference_type, "QRR")
        self.assertEqual(invoice.reference, "000000000000015850491184852")

    def tearDown(self):
        self.invoice_dict = None
