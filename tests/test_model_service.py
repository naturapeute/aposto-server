from datetime import timezone
from unittest import TestCase

from pydantic import ValidationError

from models.service import Service


class ServiceTestCase(TestCase):
    def setUp(self):
        self.service_dict: dict = {"date": 1585008000.000, "code": 1003, "duration": 45}

    def test_valid(self):
        try:
            Service(**self.service_dict)
        except ValidationError:
            self.fail("Service is invalid while it should not.")

        self.service_dict["date"] = 1585008000000

        try:
            Service(**self.service_dict)
        except ValidationError:
            self.fail("Service is invalid while it should not.")

        # FIXME : pydantic actually does not support JavaScript negative timestamp
        #           Enable this code when it will be properly parsed.
        #           See https://github.com/samuelcolvin/pydantic/issues/1600
        # self.service_dict["date"] = -1585008000000

        # try:
        #     Service(**self.service_dict)
        # except ValidationError:
        #     self.fail("Service is invalid while it should not.")

    def test_date_is_utc(self):
        service: Service = Service(**self.service_dict)

        self.assertEqual(service.date.tzinfo, timezone.utc)

    def test_quantity(self):
        service: Service = Service(**self.service_dict)

        self.assertEqual(service.quantity, 9)

    def test_amount(self):
        service_price: int = 100
        service: Service = Service(**self.service_dict)

        self.assertEqual(service.amount(service_price), 75.0)

    def test_missing_date(self):
        self.service_dict.pop("date")

        with self.assertRaises(ValidationError):
            Service(**self.service_dict)

    def test_wrong_date(self):
        self.service_dict["date"] = "test"

        with self.assertRaises(ValidationError):
            Service(**self.service_dict)

    def test_missing_duration(self):
        self.service_dict.pop("duration")

        with self.assertRaises(ValidationError):
            Service(**self.service_dict)

    def test_wrong_duration(self):
        self.service_dict["duration"] = "test"

        with self.assertRaises(ValidationError):
            Service(**self.service_dict)

        self.service_dict["duration"] = 0

        with self.assertRaises(ValidationError):
            Service(**self.service_dict)

        self.service_dict["duration"] = 7

        with self.assertRaises(ValidationError):
            Service(**self.service_dict)

    def test_missing_code(self):
        self.service_dict.pop("code")

        with self.assertRaises(ValidationError):
            Service(**self.service_dict)

    def test_wrong_code(self):
        self.service_dict["code"] = 1

        with self.assertRaises(ValidationError):
            Service(**self.service_dict)

    def tearDown(self):
        self.author_dict = None
