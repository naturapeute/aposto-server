from typing import Dict
from datetime import datetime, timezone


class ReceiptContent:
    def __init__(self, receipt_content_dict: Dict):
        self._receipt_content_dict: Dict = receipt_content_dict
        self._date: datetime = datetime.utcfromtimestamp(
            self._receipt_content_dict["timestamp"] / 1000
        ).replace(tzinfo=timezone.utc)
        self.author: Author = Author(self._receipt_content_dict["author"])
        self.therapist: Therapist = Therapist(self._receipt_content_dict["therapist"])

    @property
    def timestamp(self) -> str:
        return str(int(self._date.timestamp() * 1000))[:-3]

    @property
    def fullDateString(self) -> str:
        return self._date.strftime("%d.%m.%Y %H:%M:%S")

    @property
    def identification(self) -> str:
        return f"{self.timestamp} · {self.fullDateString}"


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
