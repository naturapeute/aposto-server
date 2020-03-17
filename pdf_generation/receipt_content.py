from typing import Dict, List
from datetime import datetime, timezone


class ReceiptContent:
    def __init__(self, receipt_content_dict: Dict):
        self._receipt_content_dict: Dict = receipt_content_dict
        self._date: datetime = self.timestamp_to_datetime(
            self._receipt_content_dict["timestamp"]
        )
        self.author: Author = Author(self._receipt_content_dict["author"])
        self.therapist: Therapist = Therapist(self._receipt_content_dict["therapist"])
        self.patient: Patient = Patient(self._receipt_content_dict["patient"])

    @property
    def timestamp(self) -> str:
        return str(int(self._date.timestamp() * 1000))[:-3]

    @property
    def full_date_string(self) -> str:
        return self._date.strftime("%d.%m.%Y %H:%M:%S")

    @property
    def identification(self) -> str:
        return f"{self.timestamp} · {self.full_date_string}"

    @property
    def page(self) -> str:
        return str(1)

    @staticmethod
    def timestamp_to_datetime(timestamp: float) -> datetime:
        return datetime.utcfromtimestamp(timestamp / 1000).replace(tzinfo=timezone.utc)


class Entity:
    def __init__(self, entity_dict: Dict):
        self._entity_dict: Dict = entity_dict

    @property
    def RCC(self) -> str:
        return self._entity_dict["RCCNumber"]

    @property
    def address(self) -> str:
        return f"{self._entity_dict['street']} · {self._entity_dict['NPA']} {self._entity_dict['city']}"

    @property
    def phone(self) -> str:
        return self._entity_dict["phone"]


class Author(Entity):
    def __init__(self, author_dict: Dict):
        super().__init__(author_dict)
        self._author_dict: Dict = author_dict

    @property
    def name(self) -> str:
        return self._author_dict["name"]


class Therapist(Entity):
    def __init__(self, therapist_dict: Dict):
        super().__init__(therapist_dict)
        self._therapist_dict: Dict = therapist_dict

    @property
    def name(self) -> str:
        return f"{self._therapist_dict['firstName']} {self._therapist_dict['lastName']}"


class Patient:
    def __init__(self, patient_dict: Dict):
        self._patient_dict: Dict = patient_dict

    @property
    def first_name(self) -> str:
        return self._patient_dict["firstName"]

    @property
    def last_name(self) -> str:
        return self._patient_dict["lastName"]

    @property
    def street(self) -> str:
        return self._patient_dict["street"]

    @property
    def NPA(self) -> str:
        return self._patient_dict["NPA"]

    @property
    def city(self) -> str:
        return self._patient_dict["city"]

    @property
    def birthdate(self) -> str:
        return ReceiptContent.timestamp_to_datetime(
            self._patient_dict["birthdate"]
        ).strftime("%d.%m.%Y")
