from typing import Dict, List
from datetime import datetime, timezone

from pdf_generation.service_codes import SERVICE_CODES


class ReceiptContent:
    def __init__(self, receipt_content_dict: Dict):
        self._receipt_content_dict: Dict = receipt_content_dict
        self._date: datetime = self.timestamp_to_datetime(
            self._receipt_content_dict["timestamp"]
        )
        self.author: Author = Author(self._receipt_content_dict["author"])
        self.therapist: Therapist = Therapist(self._receipt_content_dict["therapist"])
        self.patient: Patient = Patient(self._receipt_content_dict["patient"])
        self.init_therapy_dates()
        self.services: ServiceList = ServiceList(
            self._receipt_content_dict["services"],
            self._receipt_content_dict["servicePrice"],
        )
        self.init_total_amount()

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

    @property
    def therapy_dates(self) -> str:
        return f"{self._therapy_start_date.strftime('%d.%m.%Y')} - {self._therapy_end_date.strftime('%d.%m.%Y')}"

    @property
    def therapy_reason(self) -> str:
        return "Maladie"

    @property
    def receipt_number_and_date(self) -> str:
        return f"{self._date.strftime('%d.%m.%Y')} / {self.timestamp}"

    @property
    def total_amount_tax_rate_0(self) -> str:
        return self.total_amount

    @property
    def total_amount_tax_rate_1(self) -> str:
        return "0.00"

    @property
    def total_amount_tax_rate_2(self) -> str:
        return "0.00"

    @property
    def currency(self) -> str:
        return "CHF"

    @property
    def total_amount(self) -> str:
        return "%.2f" % self._total_amount

    @staticmethod
    def timestamp_to_datetime(timestamp: float) -> datetime:
        return datetime.utcfromtimestamp(timestamp / 1000).replace(tzinfo=timezone.utc)

    def init_therapy_dates(self):
        services_dates: List[datetime] = list(
            self.timestamp_to_datetime(service["date"])
            for service in self._receipt_content_dict["services"]
        )

        self._therapy_start_date: datetime = min(services_dates)
        self._therapy_end_date: datetime = max(services_dates)

    def init_total_amount(self):
        total_amount: float = 0

        for service in self.services.services:
            total_amount += service.float_amount

        self._total_amount: float = total_amount


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

    @property
    def names(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def npa_city(self) -> str:
        return f"{self.NPA} {self.city}"


class ServiceList:
    def __init__(self, services_dict: Dict, service_price: float):
        self.service_price: float = service_price / 12
        self.services: List[Service] = list(
            Service(service, self.service_price) for service in services_dict
        )


class Service:
    def __init__(self, service_dict: Dict, service_price: float):
        self._service_dict: Dict = service_dict
        self._service_price: float = service_price
        self._quantity: float = self._service_dict["duration"] / 5

    @property
    def date(self) -> str:
        return ReceiptContent.timestamp_to_datetime(
            self._service_dict["date"]
        ).strftime("%d.%m.%Y")

    @property
    def tarif_number(self) -> str:
        return "590"

    @property
    def code(self) -> str:
        return str(self._service_dict["code"])

    @property
    def quantity(self) -> str:
        return "%.2f" % self._quantity

    @property
    def price(self) -> str:
        return "%.2f" % self._service_price

    @property
    def float_amount(self) -> float:
        return self._quantity * self._service_price

    @property
    def amount(self) -> str:
        return "%.2f" % self.float_amount

    @property
    def code_label(self) -> str:
        return next(
            service_code["label"]
            for service_code in SERVICE_CODES
            if service_code["value"] == self._service_dict["code"]
        )
