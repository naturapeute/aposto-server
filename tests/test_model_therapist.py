from unittest import TestCase

from pydantic import ValidationError

from models import Therapist


class TherapistTestCase(TestCase):
    def setUp(self):
        self.therapist_dict: dict = {
            "firstname": "Leroy",
            "lastname": "Fréchette",
            "street": "Via delle Vigne 1",
            "zipcode": "7149",
            "city": "Vrin",
            "email": "LeroyFrechette@armyspy.com",
            "phone": "081 660 68 36",
            "rcc": "V123123",
        }

    def test_valid(self):
        try:
            Therapist(**self.therapist_dict)
        except ValidationError:
            self.fail("Therapist is invalid while it should not.")

        self.therapist_dict["phone"] = "081 660 68 36 081 660 68 36"

        try:
            Therapist(**self.therapist_dict)
        except ValidationError:
            self.fail("Therapist is invalid while it should not.")

    def test_valid_without_rcc(self):
        self.therapist_dict.pop("rcc")

        try:
            Therapist(**self.therapist_dict)
        except ValidationError:
            self.fail("Therapist is invalid while it should not.")

    def test_empty(self):
        with self.assertRaises(ValidationError):
            Therapist(**{})

    def test_missing_first_name(self):
        self.therapist_dict.pop("firstname")

        with self.assertRaises(ValidationError):
            Therapist(**self.therapist_dict)

    def test_wrong_first_name(self):
        self.therapist_dict["firstname"] = "Leroy Leroy Leroy Leroy Leroy Leroy Leroy"

        with self.assertRaises(ValidationError):
            Therapist(**self.therapist_dict)

        self.therapist_dict["firstname"] = ""

        with self.assertRaises(ValidationError):
            Therapist(**self.therapist_dict)

    def test_missing_last_name(self):
        self.therapist_dict.pop("lastname")

        with self.assertRaises(ValidationError):
            Therapist(**self.therapist_dict)

    def test_wrong_last_name(self):
        self.therapist_dict["lastname"] = "Fréchette Fréchette Fréchette Fréchette"

        with self.assertRaises(ValidationError):
            Therapist(**self.therapist_dict)

        self.therapist_dict["lastname"] = ""

        with self.assertRaises(ValidationError):
            Therapist(**self.therapist_dict)

    def test_missing_street(self):
        self.therapist_dict.pop("street")

        with self.assertRaises(ValidationError):
            Therapist(**self.therapist_dict)

    def test_wrong_street(self):
        self.therapist_dict["street"] = "Via delle Vigne 1 Via delle Vigne 1 Via"

        with self.assertRaises(ValidationError):
            Therapist(**self.therapist_dict)

        self.therapist_dict["street"] = ""

        with self.assertRaises(ValidationError):
            Therapist(**self.therapist_dict)

    def test_missing_zip(self):
        self.therapist_dict.pop("zipcode")

        with self.assertRaises(ValidationError):
            Therapist(**self.therapist_dict)

    def test_wrong_zip(self):
        self.therapist_dict["zipcode"] = "7149714971"

        with self.assertRaises(ValidationError):
            Therapist(**self.therapist_dict)

        self.therapist_dict["zipcode"] = ""

        with self.assertRaises(ValidationError):
            Therapist(**self.therapist_dict)

    def test_missing_city(self):
        self.therapist_dict.pop("city")

        with self.assertRaises(ValidationError):
            Therapist(**self.therapist_dict)

    def test_wrong_city(self):
        self.therapist_dict["city"] = "Vrin Vrin Vrin Vrin Vrin Vrin Vrin Vrin"

        with self.assertRaises(ValidationError):
            Therapist(**self.therapist_dict)

        self.therapist_dict["city"] = ""

        with self.assertRaises(ValidationError):
            Therapist(**self.therapist_dict)

    def test_missing_phone(self):
        self.therapist_dict.pop("phone")

        with self.assertRaises(ValidationError):
            Therapist(**self.therapist_dict)

    def test_wrong_phone(self):
        self.therapist_dict["phone"] = "08166068360816606836123123"

        with self.assertRaises(ValidationError):
            Therapist(**self.therapist_dict)

        self.therapist_dict["phone"] = ""

        with self.assertRaises(ValidationError):
            Therapist(**self.therapist_dict)

    def test_wrong_rcc(self):
        self.therapist_dict["rcc"] = "1123123"

        with self.assertRaises(ValidationError):
            Therapist(**self.therapist_dict)

        self.therapist_dict["rcc"] = "123123"

        with self.assertRaises(ValidationError):
            Therapist(**self.therapist_dict)

        self.therapist_dict["rcc"] = "VV23123"

        with self.assertRaises(ValidationError):
            Therapist(**self.therapist_dict)

        self.therapist_dict["rcc"] = "VVVVVVV"

        with self.assertRaises(ValidationError):
            Therapist(**self.therapist_dict)

    def tearDown(self):
        self.therapist_dict = None
