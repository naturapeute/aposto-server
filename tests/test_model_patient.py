from datetime import timezone
from unittest import TestCase

from pydantic import ValidationError

from models.patient import Patient


class PatientTestCase(TestCase):
    def setUp(self):
        self.patient_dict: dict = {
            "firstName": "Nicholas",
            "lastName": "Ailleboust",
            "street": "Tösstalstrasse 97",
            "ZIP": "8872",
            "city": "Weesen",
            "canton": "SG",
            "birthday": -1118102400.000,
            "gender": "female",
            "email": "NicholasAilleboust@teleworm.us",
        }

    def test_valid(self):
        try:
            Patient(**self.patient_dict)
        except ValidationError:
            self.fail("Patient is invalid while it should not.")

        self.patient_dict["birthday"] = 1118102400000

        try:
            Patient(**self.patient_dict)
        except ValidationError:
            self.fail("Patient is invalid while it should not.")

        # FIXME : pydantic actually does not support JavaScript negative timestamp
        #           Enable this code when it will be properly parsed.
        #           See https://github.com/samuelcolvin/pydantic/issues/1600
        # self.patient_dict["birthday"] = -1118102400000

        # try:
        #     Patient(**self.patient_dict)
        # except ValidationError:
        #     self.fail("Patient is invalid while it should not.")

    def test_empty(self):
        with self.assertRaises(ValidationError):
            Patient(**{})

    def test_missing_first_name(self):
        self.patient_dict.pop("firstName")

        with self.assertRaises(ValidationError):
            Patient(**self.patient_dict)

    def test_wrong_first_name(self):
        self.patient_dict["firstName"] = "Nicholas Nicholas Nicholas Nicholas Nicholas"

        with self.assertRaises(ValidationError):
            Patient(**self.patient_dict)

        self.patient_dict["firstName"] = ""

        with self.assertRaises(ValidationError):
            Patient(**self.patient_dict)

    def test_missing_last_name(self):
        self.patient_dict.pop("lastName")

        with self.assertRaises(ValidationError):
            Patient(**self.patient_dict)

    def test_wrong_last_name(self):
        self.patient_dict["lastName"] = "Ailleboust Ailleboust Ailleboust Ailleboust"

        with self.assertRaises(ValidationError):
            Patient(**self.patient_dict)

        self.patient_dict["lastName"] = ""

        with self.assertRaises(ValidationError):
            Patient(**self.patient_dict)

    def test_too_long_name(self):
        self.patient_dict["firstName"] = "Nicholas Nicholas Nicholas Nicholas"
        self.patient_dict["lastName"] = "Ailleboust Ailleboust Ailleboust Ai"

        with self.assertRaises(ValidationError):
            Patient(**self.patient_dict)

    def test_missing_street(self):
        self.patient_dict.pop("street")

        with self.assertRaises(ValidationError):
            Patient(**self.patient_dict)

    def test_wrong_street(self):
        self.patient_dict["street"] = "Tösstalstrasse 97 Tösstalstrasse 97 Tösstalstrasse"

        with self.assertRaises(ValidationError):
            Patient(**self.patient_dict)

        self.patient_dict["street"] = ""

        with self.assertRaises(ValidationError):
            Patient(**self.patient_dict)

    def test_missing_zip(self):
        self.patient_dict.pop("ZIP")

        with self.assertRaises(ValidationError):
            Patient(**self.patient_dict)

    def test_wrong_zip(self):
        self.patient_dict["ZIP"] = "8872887288"

        with self.assertRaises(ValidationError):
            Patient(**self.patient_dict)

        self.patient_dict["ZIP"] = ""

        with self.assertRaises(ValidationError):
            Patient(**self.patient_dict)

    def test_missing_city(self):
        self.patient_dict.pop("city")

        with self.assertRaises(ValidationError):
            Patient(**self.patient_dict)

    def test_wrong_city(self):
        self.patient_dict["city"] = "Weesen Weesen Weesen Weesen Weesen Weesen"

        with self.assertRaises(ValidationError):
            Patient(**self.patient_dict)

        self.patient_dict["city"] = ""

        with self.assertRaises(ValidationError):
            Patient(**self.patient_dict)

    def test_missing_canton(self):
        self.patient_dict.pop("canton")

        with self.assertRaises(ValidationError):
            Patient(**self.patient_dict)

    def test_wrong_canton(self):
        self.patient_dict["canton"] = "ZZ"

        with self.assertRaises(ValidationError):
            Patient(**self.patient_dict)

    def test_birthday_is_utc(self):
        invoice: Patient = Patient(**self.patient_dict)

        self.assertEqual(invoice.birthday.tzinfo, timezone.utc)

    def test_missing_birthday(self):
        self.patient_dict.pop("birthday")

        with self.assertRaises(ValidationError):
            Patient(**self.patient_dict)

    def test_wrong_birthday(self):
        self.patient_dict["birthday"] = "test"

        with self.assertRaises(ValidationError):
            Patient(**self.patient_dict)

    def test_missing_gender(self):
        self.patient_dict.pop("gender")

        with self.assertRaises(ValidationError):
            Patient(**self.patient_dict)

    def test_wrong_gender(self):
        self.patient_dict["gender"] = "test"

        with self.assertRaises(ValidationError):
            Patient(**self.patient_dict)

    def test_missing_email(self):
        self.patient_dict.pop("email")

        with self.assertRaises(ValidationError):
            Patient(**self.patient_dict)

    def test_wrong_email(self):
        self.patient_dict["email"] = "NicholasAilleboust@teleworm."

        with self.assertRaises(ValidationError):
            Patient(**self.patient_dict)

        self.patient_dict["email"] = "NicholasAilleboust@teleworm"

        with self.assertRaises(ValidationError):
            Patient(**self.patient_dict)

        self.patient_dict["email"] = "NicholasAilleboust@"

        with self.assertRaises(ValidationError):
            Patient(**self.patient_dict)

        self.patient_dict["email"] = "NicholasAilleboust"

        with self.assertRaises(ValidationError):
            Patient(**self.patient_dict)

    def tearDown(self):
        self.patient_dict = None
