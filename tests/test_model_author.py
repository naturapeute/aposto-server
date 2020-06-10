from unittest import TestCase

from pydantic import ValidationError

from models import Author


class AuthorTestCase(TestCase):
    def setUp(self):
        self.author_dict: dict = {
            "name": "Cabinet de Leroy",
            "street": "Via delle Vigne 1",
            "ZIP": "7149",
            "city": "Vrin",
            "email": "LeroyFrechette@armyspy.com",
            "phone": "081 660 68 36",
            "IBAN": "CH1231234567890123456",
            "RCC": "V123123",
        }

    def test_valid(self):
        try:
            Author(**self.author_dict)
        except ValidationError:
            self.fail("Author is invalid while it should not.")

        self.author_dict["QRIBAN"] = "CH2631234567890123456"

        try:
            Author(**self.author_dict)
        except ValidationError:
            self.fail("Author is invalid while it should not.")

        self.author_dict["phone"] = "081 660 68 36 081 660 68 36"

        try:
            Author(**self.author_dict)
        except ValidationError:
            self.fail("Author is invalid while it should not.")

    def test_valid_without_rcc(self):
        self.author_dict.pop("RCC")

        try:
            Author(**self.author_dict)
        except ValidationError:
            self.fail("Author is invalid while it should not.")

    def test_valid_without_iban(self):
        self.author_dict.pop("IBAN")

        try:
            Author(**self.author_dict)
        except ValidationError:
            self.fail("Author is invalid while it should not.")

    def test_empty(self):
        with self.assertRaises(ValidationError):
            Author(**{})

    def test_missing_name(self):
        self.author_dict.pop("name")

        with self.assertRaises(ValidationError):
            Author(**self.author_dict)

    def test_wrong_name(self):
        self.author_dict[
            "name"
        ] = "Cabinet de Leroy Cabinet de Leroy Cabinet de Leroy Cabinet de Leroy Cabinet"

        with self.assertRaises(ValidationError):
            Author(**self.author_dict)

        self.author_dict["name"] = ""

        with self.assertRaises(ValidationError):
            Author(**self.author_dict)

    def test_missing_street(self):
        self.author_dict.pop("street")

        with self.assertRaises(ValidationError):
            Author(**self.author_dict)

    def test_wrong_street(self):
        self.author_dict["street"] = "Via delle Vigne 1 Via delle Vigne 1 Via"

        with self.assertRaises(ValidationError):
            Author(**self.author_dict)

        self.author_dict["street"] = ""

        with self.assertRaises(ValidationError):
            Author(**self.author_dict)

    def test_missing_zip(self):
        self.author_dict.pop("ZIP")

        with self.assertRaises(ValidationError):
            Author(**self.author_dict)

    def test_wrong_zip(self):
        self.author_dict["ZIP"] = "7149714971"

        with self.assertRaises(ValidationError):
            Author(**self.author_dict)

        self.author_dict["ZIP"] = ""

        with self.assertRaises(ValidationError):
            Author(**self.author_dict)

    def test_missing_city(self):
        self.author_dict.pop("city")

        with self.assertRaises(ValidationError):
            Author(**self.author_dict)

    def test_wrong_city(self):
        self.author_dict["city"] = "Vrin Vrin Vrin Vrin Vrin Vrin Vrin Vrin"

        with self.assertRaises(ValidationError):
            Author(**self.author_dict)

        self.author_dict["city"] = ""

        with self.assertRaises(ValidationError):
            Author(**self.author_dict)

    def test_missing_phone(self):
        self.author_dict.pop("phone")

        with self.assertRaises(ValidationError):
            Author(**self.author_dict)

    def test_wrong_phone(self):
        self.author_dict["phone"] = "08166068360816606836123123"

        with self.assertRaises(ValidationError):
            Author(**self.author_dict)

        self.author_dict["phone"] = ""

        with self.assertRaises(ValidationError):
            Author(**self.author_dict)

    def test_missing_email(self):
        self.author_dict.pop("email")

        with self.assertRaises(ValidationError):
            Author(**self.author_dict)

    def test_wrong_email(self):
        self.author_dict["email"] = "LeroyFrechette@armyspy."

        with self.assertRaises(ValidationError):
            Author(**self.author_dict)

        self.author_dict["email"] = "LeroyFrechette@armyspy"

        with self.assertRaises(ValidationError):
            Author(**self.author_dict)

        self.author_dict["email"] = "LeroyFrechette@"

        with self.assertRaises(ValidationError):
            Author(**self.author_dict)

        self.author_dict["email"] = "LeroyFrechette"

        with self.assertRaises(ValidationError):
            Author(**self.author_dict)

    def test_wrong_rcc(self):
        self.author_dict["RCC"] = "1123123"

        with self.assertRaises(ValidationError):
            Author(**self.author_dict)

        self.author_dict["RCC"] = "123123"

        with self.assertRaises(ValidationError):
            Author(**self.author_dict)

        self.author_dict["RCC"] = "VV23123"

        with self.assertRaises(ValidationError):
            Author(**self.author_dict)

        self.author_dict["RCC"] = "VVVVVVV"

        with self.assertRaises(ValidationError):
            Author(**self.author_dict)

    def test_wrong_iban(self):
        self.author_dict["IBAN"] = "114430999123000889012"

        with self.assertRaises(ValidationError):
            Author(**self.author_dict)

        self.author_dict["IBAN"] = "AA4440999123000889012"

        with self.assertRaises(ValidationError):
            Author(**self.author_dict)

        self.author_dict["IBAN"] = "AAA430999123000889012"

        with self.assertRaises(ValidationError):
            Author(**self.author_dict)

        self.author_dict["IBAN"] = "CH44359991230008890121"

        with self.assertRaises(ValidationError):
            Author(**self.author_dict)

    def test_wrong_esr_id(self):
        self.author_dict["ESRId"] = "12345"

        with self.assertRaises(ValidationError):
            Author(**self.author_dict)

        self.author_dict["ESRId"] = "1234567"

        with self.assertRaises(ValidationError):
            Author(**self.author_dict)

        self.author_dict["ESRId"] = "AAAAAA"

        with self.assertRaises(ValidationError):
            Author(**self.author_dict)

    def test_wrong_esr_bank_id(self):
        self.author_dict["ESRBankId"] = "01123456"

        with self.assertRaises(ValidationError):
            Author(**self.author_dict)

        self.author_dict["ESRBankId"] = "0112345612"

        with self.assertRaises(ValidationError):
            Author(**self.author_dict)

        self.author_dict["ESRBankId"] = "111234561"

        with self.assertRaises(ValidationError):
            Author(**self.author_dict)

        self.author_dict["ESRBankId"] = "01AAAAAA1"

        with self.assertRaises(ValidationError):
            Author(**self.author_dict)

    def tearDown(self):
        self.author_dict = None
