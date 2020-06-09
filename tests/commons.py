from unittest import TestCase

from responses import POST, Response

from app import config


class InvoiceContentTestCase(TestCase):
    def setUp(self):
        self.invoice_content_base_64: str = "eyJuYXR1cmFwZXV0ZUlEIjoiMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwIiwiYXV0aG9yIjp7Im5hbWUiOiJDYWJpbmV0IGRlIExlcm95Iiwic3RyZWV0IjoiVmlhIGRlbGxlIFZpZ25lIDEiLCJaSVAiOiI3MTQ5IiwiY2l0eSI6IlZyaW4iLCJlbWFpbCI6Ikxlcm95RnJlY2hldHRlQGFybXlzcHkuY29tIiwicGhvbmUiOiIwODEgNjYwIDY4IDM2IiwiUkNDIjoiVjEyMzEyMyJ9LCJ0aGVyYXBpc3QiOnsiZmlyc3ROYW1lIjoiTGVyb3kiLCJsYXN0TmFtZSI6IkZy6WNoZXR0ZSIsInN0cmVldCI6IlZpYSBkZWxsZSBWaWduZSAxIiwiWklQIjoiNzE0OSIsImNpdHkiOiJWcmluIiwiZW1haWwiOiJMZXJveUZyZWNoZXR0ZUBhcm15c3B5LmNvbSIsInBob25lIjoiMDgxIDY2MCA2OCAzNiIsIlJDQyI6IlYxMjMxMjMifSwicGF0aWVudCI6eyJfaWQiOiIxNTg1MDQ4NzU4ODkwIiwiZmlyc3ROYW1lIjoiTmljaG9sYXMiLCJsYXN0TmFtZSI6IkFpbGxlYm91c3QiLCJzdHJlZXQiOiJU9nNzdGFsc3RyYXNzZSA5NyIsIlpJUCI6Ijg4NzIiLCJjaXR5IjoiV2Vlc2VuIiwiY2FudG9uIjoiU0ciLCJiaXJ0aGRheSI6LTExMTgxMDI0MDAwMDAsImdlbmRlciI6ImZlbWFsZSIsImVtYWlsIjoiTmljaG9sYXNBaWxsZWJvdXN0QHRlbGV3b3JtLnVzIn0sInNlcnZpY2VQcmljZSI6MTAwLCJzZXJ2aWNlcyI6W3siZGF0ZSI6MTU4NTAwODAwMDAwMCwiY29kZSI6MTAwMywiZHVyYXRpb24iOjYwfV0sInRpbWVzdGFtcCI6MTU4NTA0OTExODQ4NX0="
        self.invoice_content_dict: dict = {
            "naturapeuteID": "000000000000000000000000",
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
                "_id": "1585048758890",
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
        self.invoice_content_base_64 = None
        self.invoice_content_dict = None


class InvoiceContentDemoModeTestCase(TestCase):
    def setUp(self):
        self.invoice_content_demo_base_64: str = "eyJhdXRob3IiOnsibmFtZSI6IkNhYmluZXQgZGUgTGVyb3kiLCJzdHJlZXQiOiJWaWEgZGVsbGUgVmlnbmUgMSIsIlpJUCI6IjcxNDkiLCJjaXR5IjoiVnJpbiIsImVtYWlsIjoiTGVyb3lGcmVjaGV0dGVAYXJteXNweS5jb20iLCJwaG9uZSI6IjA4MSA2NjAgNjggMzYiLCJSQ0MiOiJWMTIzMTIzIn0sInRoZXJhcGlzdCI6eyJmaXJzdE5hbWUiOiJMZXJveSIsImxhc3ROYW1lIjoiRnLpY2hldHRlIiwic3RyZWV0IjoiVmlhIGRlbGxlIFZpZ25lIDEiLCJaSVAiOiI3MTQ5IiwiY2l0eSI6IlZyaW4iLCJlbWFpbCI6Ikxlcm95RnJlY2hldHRlQGFybXlzcHkuY29tIiwicGhvbmUiOiIwODEgNjYwIDY4IDM2IiwiUkNDIjoiVjEyMzEyMyJ9LCJwYXRpZW50Ijp7Il9pZCI6IjE1ODUwNDg3NTg4OTAiLCJmaXJzdE5hbWUiOiJOaWNob2xhcyIsImxhc3ROYW1lIjoiQWlsbGVib3VzdCIsInN0cmVldCI6IlT2c3N0YWxzdHJhc3NlIDk3IiwiWklQIjoiODg3MiIsImNpdHkiOiJXZWVzZW4iLCJjYW50b24iOiJTRyIsImJpcnRoZGF5IjotMTExODEwMjQwMDAwMCwiZ2VuZGVyIjoiZmVtYWxlIiwiZW1haWwiOiJOaWNob2xhc0FpbGxlYm91c3RAdGVsZXdvcm0udXMifSwic2VydmljZVByaWNlIjoxMDAsInNlcnZpY2VzIjpbeyJkYXRlIjoxNTg1MDA4MDAwMDAwLCJjb2RlIjoxMDAzLCJkdXJhdGlvbiI6NjB9XSwidGltZXN0YW1wIjoxNTg1MDQ5MTE4NDg1fQ=="
        self.invoice_content_demo_dict: dict = {
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
                "_id": "1585048758890",
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
        self.invoice_content_demo_base_64 = None
        self.invoice_content_demo_dict = None


class InvoiceContentImproperBase64TestCase(TestCase):
    FAILURE_JSON = {"error": "Improper base64 provided"}

    def setUp(self):
        self.invoice_content_improper_base_base_64: str = "azeaze"

    def tearDown(self):
        self.invoice_content_improper_base_base_64 = None


class InvoiceContentImproperJSONTestCase(TestCase):
    FAILURE_JSON = {"error": "Improper JSON provided inside base64"}

    def setUp(self):
        self.invoice_content_improper_json_base_64: str = "dGVzdA=="

    def tearDown(self):
        self.invoice_content_improper_json_base_64 = None


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
                "_id": "1585048758890",
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
