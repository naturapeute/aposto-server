from unittest import TestCase

from pydantic import ValidationError

from models.author import Author


class AuthorTestCase(TestCase):
    def setUp(self):
        self.author_dict: dict = {
            "name": "Cabinet de Leroy",
            "street": "Via delle Vigne 1",
            "ZIP": "7149",
            "city": "Vrin",
            "email": "LeroyFrechette@armyspy.com",
            "phone": "081 660 68 36",
            "RCC": "V123123",
        }

    def test_valid(self):
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

    def test_empty(self):
        with self.assertRaises(ValidationError):
            Author(**{})

    def test_missing_name(self):
        self.author_dict.pop("name")

        with self.assertRaises(ValidationError):
            Author(**self.author_dict)

    def test_too_long_name(self):
        self.author_dict[
            "name"
        ] = "Cabinet de Leroy Cabinet de Leroy Cabinet de Leroy Cabinet de Leroy Cabinet"

        with self.assertRaises(ValidationError):
            Author(**self.author_dict)

    def test_missing_street(self):
        self.author_dict.pop("street")

        with self.assertRaises(ValidationError):
            Author(**self.author_dict)

    def test_too_long_street(self):
        self.author_dict[
            "street"
        ] = "Via delle Vigne 1 Via delle Vigne 1 Via delle Vigne 1 Via delle Vigne 1"

        with self.assertRaises(ValidationError):
            Author(**self.author_dict)

    def test_missing_zip(self):
        self.author_dict.pop("ZIP")

        with self.assertRaises(ValidationError):
            Author(**self.author_dict)

    def test_too_long_zip(self):
        self.author_dict["ZIP"] = "7149 7149 7149 7149"

        with self.assertRaises(ValidationError):
            Author(**self.author_dict)

    def test_missing_city(self):
        self.author_dict.pop("city")

        with self.assertRaises(ValidationError):
            Author(**self.author_dict)

    def test_too_long_city(self):
        self.author_dict["city"] = "Vrin Vrin Vrin Vrin Vrin Vrin Vrin Vrin"

        with self.assertRaises(ValidationError):
            Author(**self.author_dict)

    def test_missing_phone(self):
        self.author_dict.pop("phone")

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

    def tearDown(self):
        self.author_dict = None
