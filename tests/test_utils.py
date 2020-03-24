from typing import Dict
from unittest import TestCase

from app import parse_invoice_content
from pdf_generation.invoice_content import InvoiceContent


class UtilsTest(TestCase):
    def setUp(self):
        self.invoice_content_base64: str = "eyJpbnRSYW5kb20iOjgzLCJhdXRob3IiOnsibmFtZSI6IkNhYmluZXQgZGUgTGVyb3kiLCJzdHJlZXQiOiJWaWEgZGVsbGUgVmlnbmUgMSIsIlpJUCI6IjcxNDkiLCJjaXR5IjoiVnJpbiIsImVtYWlsIjoiTGVyb3lGcmVjaGV0dGVAYXJteXNweS5jb20iLCJwaG9uZSI6IjA4MSA2NjAgNjggMzYiLCJSQ0NOdW1iZXIiOiJWMTIzMTIzIiwiR0xOTnVtYmVyIjoiNzYwMTIwMjQzMTMxMSJ9LCJ0aGVyYXBpc3QiOnsiZmlyc3ROYW1lIjoiTGVyb3kiLCJsYXN0TmFtZSI6IkZy6WNoZXR0ZSIsInN0cmVldCI6IlZpYSBkZWxsZSBWaWduZSAxIiwiWklQIjoiNzE0OSIsImNpdHkiOiJWcmluIiwiZW1haWwiOiJMZXJveUZyZWNoZXR0ZUBhcm15c3B5LmNvbSIsInBob25lIjoiMDgxIDY2MCA2OCAzNiIsIlJDQ051bWJlciI6IlYxMjMxMjMiLCJHTE5OdW1iZXIiOiI3NjAxMjAyNDMxMzExIn0sInBhdGllbnQiOnsiX2lkIjoiMTU4NTA0ODc1ODg5MCIsImZpcnN0TmFtZSI6Ik5pY2hvbGFzIiwibGFzdE5hbWUiOiJBaWxsZWJvdXN0Iiwic3RyZWV0IjoiVPZzc3RhbHN0cmFzc2UgOTciLCJaSVAiOiI4ODcyIiwiY2l0eSI6IldlZXNlbiIsImNhbnRvbiI6IlNHIiwiYmlydGhkYXRlIjotMTExODEwMjQwMDAwMCwiZ2VuZGVyIjoiZmVtYWxlIiwiZW1haWwiOiJOaWNob2xhc0FpbGxlYm91c3RAdGVsZXdvcm0udXMifSwic2VydmljZVByaWNlIjoxMDAsInNlcnZpY2VzIjpbeyJkYXRlIjoxNTg1MDA4MDAwMDAwLCJjb2RlIjoxMDAzLCJkdXJhdGlvbiI6NjB9XSwidGltZXN0YW1wIjoxNTg1MDQ5MTE4NDg1fQ=="
        self.invoice_content_dict: Dict = {
            "intRandom": 83,
            "author": {
                "name": "Cabinet de Leroy",
                "street": "Via delle Vigne 1",
                "ZIP": "7149",
                "city": "Vrin",
                "email": "LeroyFrechette@armyspy.com",
                "phone": "081 660 68 36",
                "RCCNumber": "V123123",
                "GLNNumber": "7601202431311",
            },
            "therapist": {
                "firstName": "Leroy",
                "lastName": "Fréchette",
                "street": "Via delle Vigne 1",
                "ZIP": "7149",
                "city": "Vrin",
                "email": "LeroyFrechette@armyspy.com",
                "phone": "081 660 68 36",
                "RCCNumber": "V123123",
                "GLNNumber": "7601202431311",
            },
            "patient": {
                "_id": "1585048758890",
                "firstName": "Nicholas",
                "lastName": "Ailleboust",
                "street": "Tösstalstrasse 97",
                "ZIP": "8872",
                "city": "Weesen",
                "canton": "SG",
                "birthdate": -1118102400000,
                "gender": "female",
                "email": "NicholasAilleboust@teleworm.us",
            },
            "servicePrice": 100,
            "services": [{"date": 1585008000000, "code": 1003, "duration": 60}],
            "timestamp": 1585049118485,
        }

    def test_parse_invoice_content(self):
        invoice_content: InvoiceContent = parse_invoice_content(
            self.invoice_content_base64
        )

        self.assertDictEqual(
            invoice_content._invoice_content_dict, self.invoice_content_dict
        )

    def tearDown(self):
        self.invoice_content_base64 = None
        self.invoice_content_dict = None
