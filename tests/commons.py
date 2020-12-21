from unittest import TestCase

from responses import POST, Response

from app import config


class InvoiceContentTestCase(TestCase):
    def setUp(self):
        self.invoice: dict = {
            "id": "000000000000000000000000",
            "author": {
                "name": "Cabinet de Leroy",
                "street": "Via delle Vigne 1",
                "zipcode": "7149",
                "city": "Vrin",
                "email": "LeroyFrechette@armyspy.com",
                "phone": "081 660 68 36",
                "rcc": "V123123",
                "iban": "CH5131234567890123456",
            },
            "therapist": {
                "firstname": "Leroy",
                "lastname": "Fréchette",
                "street": "Via delle Vigne 1",
                "zipcode": "7149",
                "city": "Vrin",
                "phone": "081 660 68 36",
                "rcc": "V123123",
            },
            "patient": {
                "firstname": "Nicholas",
                "lastname": "Ailleboust",
                "street": "Tösstalstrasse 97",
                "zipcode": "8872",
                "city": "Weesen",
                "canton": "SG",
                "birthdate": -1118102400,
                "gender": "woman",
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

    def tearDown(self):
        self.invoice = None


class InvoiceContentDemoModeTestCase(TestCase):
    def setUp(self):
        self.invoice_demo: str = {
            "author": {
                "name": "Cabinet de Leroy",
                "street": "Via delle Vigne 1",
                "zipcode": "7149",
                "city": "Vrin",
                "email": "LeroyFrechette@armyspy.com",
                "phone": "081 660 68 36",
                "rcc": "V123123",
                "iban": "CH5131234567890123456",
            },
            "therapist": {
                "firstname": "Leroy",
                "lastname": "Fréchette",
                "street": "Via delle Vigne 1",
                "zipcode": "7149",
                "city": "Vrin",
                "phone": "081 660 68 36",
                "rcc": "V123123",
            },
            "patient": {
                "firstname": "Nicholas",
                "lastname": "Ailleboust",
                "street": "Tösstalstrasse 97",
                "zipcode": "8872",
                "city": "Weesen",
                "canton": "SG",
                "birthdate": -1118102400,
                "gender": "woman",
                "email": "NicholasAilleboust@teleworm.us",
            },
            "servicePrice": 100,
            "services": [
                {"date": 1584921600000, "code": 1003, "duration": 60},
                {"date": 1585008000000, "code": 1004, "duration": 30},
            ],
            "timestamp": 1585049118.485,
            "paid": False,
        }

    def tearDown(self):
        self.invoice_demo = None


class InvoiceContentInvalidTestCase(TestCase):
    FAILURE_JSON = [
        {
            "loc": ["author", "name"],
            "msg": "field required",
            "type": "value_error.missing",
        },
        {
            "loc": ["author", "zipcode"],
            "msg": "ensure this value has at most 9 characters",
            "type": "value_error.any_str.max_length",
            "ctx": {"limit_value": 9},
        },
        {
            "loc": ["author", "rcc"],
            "msg": 'string does not match regex "^[A-Z][0-9]{6}$"',
            "type": "value_error.str.regex",
            "ctx": {"pattern": "^[A-Z][0-9]{6}$"},
        },
        {
            "loc": ["patient", "email"],
            "msg": "value is not a valid email address",
            "type": "value_error.email",
        },
    ]

    def setUp(self):
        self.invoice_invalid: str = {
            "id": "000000000000000000000000",
            "author": {
                "street": "Via delle Vigne 1",
                "zipcode": "7149 7149 7149 7149",
                "city": "Vrin",
                "email": "LeroyFrechette@armyspy.com",
                "phone": "081 660 68 36",
                "rcc": "V12312",
                "iban": "CH5131234567890123456",
            },
            "therapist": {
                "firstname": "Leroy",
                "lastname": "Fréchette",
                "street": "Via delle Vigne 1",
                "zipcode": "7149",
                "city": "Vrin",
                "phone": "081 660 68 36",
                "rcc": "V123123",
            },
            "patient": {
                "firstname": "Nicholas",
                "lastname": "Ailleboust",
                "street": "Tösstalstrasse 97",
                "zipcode": "8872",
                "city": "Weesen",
                "canton": "SG",
                "birthdate": -1118102400,
                "gender": "woman",
                "email": "NicholasAilleboust@teleworm.",
            },
            "servicePrice": 100,
            "services": [
                {"date": 1584921600000, "code": 1003, "duration": 60},
                {"date": 1585008000000, "code": 1004, "duration": 30},
            ],
            "timestamp": 1585049118.485,
            "paid": False,
        }

    def tearDown(self):
        self.invoice_invalid = None


class InvoiceContentImproperJSONTestCase(TestCase):
    FAILURE_JSON = {
        "json_error": "Expecting property name enclosed in double quotes: line 1 column 2 (char 1)"
    }

    def setUp(self):
        self.invoice_improper_json: str = '{id:"000000000000000000000000"}'

    def tearDown(self):
        self.invoice_improper_json = None


class SendInBlueMock:
    FAILURE_JSON: dict = {"code": "400", "message": "Invalid parameter"}

    @staticmethod
    def smtp_email_success_request() -> Response:
        return Response(
            POST,
            f"{config['sendInBlueAPIURL']}/smtp/email",
            json={"messageId": "1"},
            status=201,
        )

    @staticmethod
    def smtp_email_failure_request() -> Response:
        return Response(
            POST,
            f"{config['sendInBlueAPIURL']}/smtp/email",
            json=SendInBlueMock.FAILURE_JSON,
            status=400,
        )
