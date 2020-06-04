from unittest import TestCase

from pydantic import ValidationError

from models.therapist import Therapist


class TherapistTestCase(TestCase):
    def setUp(self):
        self.therapist_dict: dict = {
            "firstName": "Leroy",
            "lastName": "Fréchette",
            "street": "Via delle Vigne 1",
            "ZIP": "7149",
            "city": "Vrin",
            "email": "LeroyFrechette@armyspy.com",
            "phone": "081 660 68 36",
            "RCC": "V123123",
        }

    def test_valid(self):
        try:
            Therapist.parse_obj(self.therapist_dict)
        except ValidationError:
            self.fail("Therapist is invalid while it should not.")

    def test_valid_without_rcc(self):
        self.therapist_dict.pop("RCC")

        try:
            Therapist.parse_obj(self.therapist_dict)
        except ValidationError:
            self.fail("Therapist is invalid while it should not.")

    def test_empty(self):
        with self.assertRaises(ValidationError):
            Therapist.parse_obj({})

    def test_missing_first_name(self):
        self.therapist_dict.pop("firstName")

        with self.assertRaises(ValidationError):
            Therapist.parse_obj(self.therapist_dict)

    def test_missing_last_name(self):
        self.therapist_dict.pop("lastName")

        with self.assertRaises(ValidationError):
            Therapist.parse_obj(self.therapist_dict)

    def test_missing_street(self):
        self.therapist_dict.pop("street")

        with self.assertRaises(ValidationError):
            Therapist.parse_obj(self.therapist_dict)

    def test_missing_zip(self):
        self.therapist_dict.pop("ZIP")

        with self.assertRaises(ValidationError):
            Therapist.parse_obj(self.therapist_dict)

    def test_missing_city(self):
        self.therapist_dict.pop("city")

        with self.assertRaises(ValidationError):
            Therapist.parse_obj(self.therapist_dict)

    def test_missing_phone(self):
        self.therapist_dict.pop("phone")

        with self.assertRaises(ValidationError):
            Therapist.parse_obj(self.therapist_dict)

    def test_wrong_rcc(self):
        self.therapist_dict["RCC"] = "1123123"

        with self.assertRaises(ValidationError):
            Therapist.parse_obj(self.therapist_dict)

        self.therapist_dict["RCC"] = "123123"

        with self.assertRaises(ValidationError):
            Therapist.parse_obj(self.therapist_dict)

        self.therapist_dict["RCC"] = "VV23123"

        with self.assertRaises(ValidationError):
            Therapist.parse_obj(self.therapist_dict)

        self.therapist_dict["RCC"] = "VVVVVVV"

        with self.assertRaises(ValidationError):
            Therapist.parse_obj(self.therapist_dict)

    def tearDown(self):
        self.therapist_dict = None
