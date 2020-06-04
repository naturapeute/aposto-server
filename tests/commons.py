from unittest import TestCase

from responses import POST, Response

from app import config


class InvoiceContentTestCase(TestCase):
    def setUp(self):
        self.invoice_json: str = '{"terrapeuteID":"000000000000000000000000","author":{"name":"Cabinet de Leroy","street":"Via delle Vigne 1","ZIP":"7149","city":"Vrin","email":"LeroyFrechette@armyspy.com","phone":"081 660 68 36","RCC":"V123123"},"therapist":{"firstName":"Leroy","lastName":"Fréchette","street":"Via delle Vigne 1","ZIP":"7149","city":"Vrin","phone":"081 660 68 36","RCC":"V123123"},"patient":{"firstName":"Nicholas","lastName":"Ailleboust","street":"Tösstalstrasse 97","ZIP":"8872","city":"Weesen","canton":"SG","birthday":-1118102400,"gender":"female","email":"NicholasAilleboust@teleworm.us"},"servicePrice":100,"services":[{"date":1584921600000,"code":1003,"duration":60},{"date":1585008000000,"code":1004,"duration":30}],"timestamp":1585049118.485}'

    def tearDown(self):
        self.invoice_json = None


class InvoiceContentDemoModeTestCase(TestCase):
    def setUp(self):
        self.invoice_demo_json: str = '{"author":{"name":"Cabinet de Leroy","street":"Via delle Vigne 1","ZIP":"7149","city":"Vrin","email":"LeroyFrechette@armyspy.com","phone":"081 660 68 36","RCC":"V123123"},"therapist":{"firstName":"Leroy","lastName":"Fréchette","street":"Via delle Vigne 1","ZIP":"7149","city":"Vrin","phone":"081 660 68 36","RCC":"V123123"},"patient":{"firstName":"Nicholas","lastName":"Ailleboust","street":"Tösstalstrasse 97","ZIP":"8872","city":"Weesen","canton":"SG","birthday":-1118102400,"gender":"female","email":"NicholasAilleboust@teleworm.us"},"servicePrice":100,"services":[{"date":1584921600000,"code":1003,"duration":60},{"date":1585008000000,"code":1004,"duration":30}],"timestamp":1585049118.485}'

    def tearDown(self):
        self.invoice_demo_json = None


class InvoiceContentInvalidTestCase(TestCase):
    FAILURE_JSON = '[\n  {\n    "loc": [\n      "author",\n      "name"\n    ],\n    "msg": "field required",\n    "type": "value_error.missing"\n  },\n  {\n    "loc": [\n      "author",\n      "ZIP"\n    ],\n    "msg": "ensure this value has at most 16 characters",\n    "type": "value_error.any_str.max_length",\n    "ctx": {\n      "limit_value": 16\n    }\n  },\n  {\n    "loc": [\n      "author",\n      "RCC"\n    ],\n    "msg": "string does not match regex \\"^[A-Z][0-9]{6}$\\"",\n    "type": "value_error.str.regex",\n    "ctx": {\n      "pattern": "^[A-Z][0-9]{6}$"\n    }\n  },\n  {\n    "loc": [\n      "patient",\n      "email"\n    ],\n    "msg": "value is not a valid email address",\n    "type": "value_error.email"\n  }\n]'

    def setUp(self):
        self.invoice_invalid_json: str = '{"terrapeuteID":"000000000000000000000000","author":{"street":"Via delle Vigne 1","ZIP":"7149 7149 7149 7149","city":"Vrin","email":"LeroyFrechette@armyspy.com","phone":"081 660 68 36","RCC":"V12312"},"therapist":{"firstName":"Leroy","lastName":"Fréchette","street":"Via delle Vigne 1","ZIP":"7149","city":"Vrin","phone":"081 660 68 36","RCC":"V123123"},"patient":{"firstName":"Nicholas","lastName":"Ailleboust","street":"Tösstalstrasse 97","ZIP":"8872","city":"Weesen","canton":"SG","birthday":-1118102400,"gender":"female","email":"NicholasAilleboust@teleworm."},"servicePrice":100,"services":[{"date":1584921600000,"code":1003,"duration":60},{"date":1585008000000,"code":1004,"duration":30}],"timestamp":1585049118.485}'

    def tearDown(self):
        self.invoice_invalid_json = None


class InvoiceContentImproperJSONTestCase(TestCase):
    FAILURE_JSON = '[\n  {\n    "loc": [\n      "__root__"\n    ],\n    "msg": "Expecting property name enclosed in double quotes: line 1 column 2 (char 1)",\n    "type": "value_error.jsondecode",\n    "ctx": {\n      "msg": "Expecting property name enclosed in double quotes",\n      "doc": "{terrapeuteID:\\"000000000000000000000000\\"}",\n      "pos": 1,\n      "lineno": 1,\n      "colno": 2\n    }\n  }\n]'

    def setUp(self):
        self.invoice_improper_json: str = '{terrapeuteID:"000000000000000000000000"}'

    def tearDown(self):
        self.invoice_improper_json = None


class InvoiceContentMissingParamTestCase(TestCase):
    FAILURE_JSON = {"author.name": "Missing parameter"}

    def setUp(self):
        self.invoice_content_missing_param_dict: dict = {
            "author": {
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
                "birthday": -1118102400000,
                "gender": "female",
                "email": "NicholasAilleboust@teleworm.us",
            },
            "servicePrice": 100,
            "services": [{"date": 1585008000000, "code": 1003, "duration": 60}],
            "timestamp": 1585049118485,
        }

    def tearDown(self):
        self.invoice_content_missing_param_dict = None


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
