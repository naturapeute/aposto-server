import base64
from datetime import datetime, timezone
from typing import Dict, List, Union

import ujson
from dateutil import tz
from PIL import Image
from pystrich.datamatrix import DataMatrixEncoder, DataMatrixRenderer

from pdf_generation.service_codes import SERVICE_CODES


class InvoiceContent:
    SCHEMA: Dict = {
        "author": {
            "name": {},
            "street": {},
            "ZIP": {},
            "city": {},
            "phone": {},
            "email": {},
            "RCC": {},
        },
        "therapist": {
            "firstName": {},
            "lastName": {},
            "street": {},
            "ZIP": {},
            "city": {},
            "phone": {},
            "RCC": {},
        },
        "patient": {
            "firstName": {},
            "lastName": {},
            "street": {},
            "ZIP": {},
            "city": {},
            "canton": {},
            "birthday": {},
            "gender": {},
            "email": {},
        },
        "servicePrice": {},
        "services": [{"date": {}, "duration": {}, "code": {}}],
        "timestamp": {},
    }

    def __init__(self, invoice_content_dict: Dict):
        self._invoice_content_dict: Dict = invoice_content_dict
        self._date: datetime = self.timestamp_to_datetime(
            self._invoice_content_dict["timestamp"]
        )
        self.author: Author = Author(self._invoice_content_dict["author"])
        self.therapist: Therapist = Therapist(self._invoice_content_dict["therapist"])
        self.patient: Patient = Patient(self._invoice_content_dict["patient"])
        self.init_therapy_dates()
        self.services: ServiceList = ServiceList(
            self._invoice_content_dict["services"],
            self._invoice_content_dict["servicePrice"],
        )
        self.init_total_amount()

    @property
    def terrapeute_id(self) -> str:
        return self._invoice_content_dict.get("terrapeuteID", None)

    @property
    def timestamp(self) -> str:
        return str(int(self._date.timestamp() * 1000))[:-3]

    @property
    def full_date_string(self) -> str:
        return self._date.astimezone(tz.gettz("Europe/Zurich")).strftime(
            "%d.%m.%Y %H:%M:%S"
        )

    @property
    def date_string(self) -> str:
        return self._date.astimezone(tz.gettz("Europe/Zurich")).strftime("%d.%m.%Y")

    @property
    def identification(self) -> str:
        return f"{self.timestamp} · {self.full_date_string}"

    @property
    def page(self) -> str:
        return str(1)

    @property
    def therapy_dates(self) -> str:
        return f"{self._therapy_start_date.astimezone(tz.gettz('Europe/Zurich')).strftime('%d.%m.%Y')} - {self._therapy_end_date.astimezone(tz.gettz('Europe/Zurich')).strftime('%d.%m.%Y')}"

    @property
    def therapy_reason(self) -> str:
        return "Maladie"

    @property
    def invoice_number_and_date(self) -> str:
        return f"{self._date.strftime('%d.%m.%Y')} / {self.timestamp}"

    @property
    def gln_list(self) -> str:
        return f"1/{self.author.gln} 2/{self.therapist.gln}"

    @property
    def total_amount_medical(self) -> str:
        return self.total_amount

    @property
    def total_amount_medicines(self) -> str:
        return "0.00"

    @property
    def total_amount_laboratory(self) -> str:
        return "0.00"

    @property
    def total_amount_medical_device(self) -> str:
        return "0.00"

    @property
    def total_amount_other(self) -> str:
        return "0.00"

    @property
    def total_amount_tax_rate_0(self) -> str:
        return self.total_amount

    @property
    def tax_rate_0_amount(self) -> str:
        return "0.00"

    @property
    def total_amount_tax_rate_1(self) -> str:
        return "0.00"

    @property
    def tax_rate_1_amount(self) -> str:
        return "0.00"

    @property
    def total_amount_tax_rate_2(self) -> str:
        return "0.00"

    @property
    def tax_rate_2_amount(self) -> str:
        return "0.00"

    @property
    def total_amount_tax_rate(self) -> str:
        return "0.00"

    @property
    def currency(self) -> str:
        return "CHF"

    @property
    def total_amount(self) -> str:
        return "%.2f" % self._total_amount

    @property
    def paid_amount(self) -> str:
        return self.total_amount

    @property
    def owed_amount(self) -> str:
        return "0.00"

    @property
    def qr_reference(self) -> Union[str, None]:
        # TODO : Update when moving to QR-invoice
        _qr_reference: Union[str, None] = self._invoice_content_dict.get(
            "QRReference", None
        )

        if _qr_reference:
            _qr_reference: str = _qr_reference.replace(" ", "")
            _qr_reference: str = " ".join(
                [_qr_reference[0:2]]
                + [_qr_reference[i : i + 5] for i in range(2, len(_qr_reference), 5)]
            )

        return _qr_reference

    @staticmethod
    def timestamp_to_datetime(timestamp: float) -> datetime:
        return datetime.utcfromtimestamp(timestamp / 1000).replace(tzinfo=timezone.utc)

    @staticmethod
    def validate(invoice_content_dict: Dict):
        missing_param: Dict = {}

        for attr, value in InvoiceContent.SCHEMA.items():
            if not attr in invoice_content_dict:
                missing_param[attr] = "Missing parameter"
                continue

            if isinstance(value, list):
                if not isinstance(invoice_content_dict[attr], list):
                    missing_param[attr] = "List expected"
                    continue

                for i, elem in enumerate(invoice_content_dict[attr]):
                    for sub_attr, _ in value[0].items():
                        if not sub_attr in elem:
                            missing_param[f"{attr}[{i}].{sub_attr}"] = "Missing parameter"
                continue

            for sub_attr, _ in InvoiceContent.SCHEMA[attr].items():
                if not sub_attr in invoice_content_dict[attr]:
                    missing_param[f"{attr}.{sub_attr}"] = "Missing parameter"

        if missing_param:
            raise ValueError(missing_param)

    @staticmethod
    def parse(invoice_content_base_64: str) -> Dict:
        return ujson.loads(base64.b64decode(invoice_content_base_64).decode("latin1"))

    def init_therapy_dates(self):
        services_dates: List[datetime] = list(
            self.timestamp_to_datetime(service["date"])
            for service in self._invoice_content_dict["services"]
        )

        self._therapy_start_date: datetime = min(services_dates)
        self._therapy_end_date: datetime = max(services_dates)

    def init_total_amount(self):
        total_amount: float = 0

        for service in self.services.services:
            total_amount += service.float_amount

        self._total_amount: float = total_amount

    def generate_datamatrix_string(self) -> Union[str, None]:
        # TODO : Update when moving to QR-invoice
        if not self.author.esr_coding_line or not self.patient.ssn:
            return None

        separator: str = "#"
        therapy_start_date = self._therapy_start_date.astimezone(
            tz.gettz("Europe/Zurich")
        ).strftime("%d.%m.%Y")
        due_amount: str = "0"

        datamatrix_string = f"{self.author.esr_coding_line}{separator}{self.author.gln}{separator}{self.therapist.gln}{separator}"
        datamatrix_string = f"{datamatrix_string}{therapy_start_date}{separator}{self.patient.ssn}{separator}{self.patient.birthday}{separator}"
        datamatrix_string = f"{datamatrix_string}{due_amount}{separator}"

        for service in self.services.services:
            datamatrix_string = (
                f"{datamatrix_string}{int(service.float_amount) % 10}{separator}"
            )

        if len(datamatrix_string) > 169:
            datamatrix_string = datamatrix_string[-169:]
        elif len(datamatrix_string) < 169:
            datamatrix_string = datamatrix_string.ljust(169, "0")

        return datamatrix_string

    def generate_datamatrix(self) -> Union[Image.Image, None]:
        datamatrix_string: str = self.generate_datamatrix_string()

        # TODO : Update when moving to QR-invoice
        if not datamatrix_string:
            return None

        encoder: DataMatrixEncoder = DataMatrixEncoder(datamatrix_string)
        renderer: DataMatrixRenderer = DataMatrixRenderer(encoder.matrix, encoder.regions)

        return renderer.get_pilimage(10)


class Entity:
    def __init__(self, entity_dict: dict):
        self._entity_dict: dict = entity_dict

    @property
    def gln(self) -> str:
        return "2099999999999"

    @property
    def rcc(self) -> str:
        return self._entity_dict["RCC"]

    @property
    def street(self) -> str:
        return self._entity_dict["street"]

    @property
    def zip_city(self) -> str:
        return f"{self._entity_dict['ZIP']} {self._entity_dict['city']}"

    @property
    def address(self) -> str:
        return f"{self.street} · {self.zip_city}"

    @property
    def phone(self) -> str:
        return self._entity_dict["phone"]

    @property
    def phone_with_header(self) -> str:
        return f"Tél.  {self._entity_dict['phone']}"


class Author(Entity):
    def __init__(self, author_dict: dict):
        super().__init__(author_dict)
        self._author_dict: dict = author_dict

    @property
    def name(self) -> str:
        return self._author_dict["name"]

    @property
    def email(self) -> str:
        return self._author_dict["email"]

    @property
    def qr_iban(self) -> Union[str, None]:
        # TODO : Update when moving to QR-invoice
        _qr_iban: Union[str, None] = self._author_dict.get("QRIBAN", None)

        if _qr_iban:
            _qr_iban: str = _qr_iban.replace(" ", "")
            _qr_iban: str = " ".join(
                [_qr_iban[i : i + 4] for i in range(0, len(_qr_iban), 4)]
            )

        return _qr_iban

    @property
    def esr_coding_line(self) -> Union[str, None]:
        # TODO : Update when moving to QR-invoice
        return self._author_dict.get("ESR", None)


class Therapist(Entity):
    def __init__(self, therapist_dict: dict):
        super().__init__(therapist_dict)
        self._therapist_dict: dict = therapist_dict

    @property
    def name(self) -> str:
        return f"{self._therapist_dict['firstName']} {self._therapist_dict['lastName']}"


class Patient:
    def __init__(self, patient_dict: dict):
        self._patient_dict: dict = patient_dict

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
    def zip(self) -> str:
        return self._patient_dict["ZIP"]

    @property
    def city(self) -> str:
        return self._patient_dict["city"]

    @property
    def birthday(self) -> str:
        return InvoiceContent.timestamp_to_datetime(
            self._patient_dict["birthday"]
        ).strftime("%d.%m.%Y")

    @property
    def gender(self) -> str:
        if self._patient_dict["gender"] == "male":
            return "H"
        else:
            return "F"

    @property
    def canton(self) -> str:
        return self._patient_dict["canton"]

    @property
    def name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def zip_city(self) -> str:
        return f"{self.zip} {self.city}"

    @property
    def email(self) -> str:
        return self._patient_dict["email"]

    @property
    def ssn(self) -> Union[str, None]:
        # TODO : Update when SSN is available
        return self._patient_dict.get("SSN", None)

    @property
    def birthday_with_header_and_gender(self) -> str:
        return f"Date de naissance {self.birthday}/{self.gender}"


class ServiceList:
    def __init__(self, services_dict: dict, service_price: float):
        self.service_price: float = service_price / 12
        self.services: List[Service] = list(
            Service(service, self.service_price) for service in services_dict
        )


class Service:
    def __init__(self, service_dict: dict, service_price: float):
        self._service_dict: dict = service_dict
        self._service_price: float = service_price
        self._quantity: float = self._service_dict["duration"] / 5

    @property
    def date(self) -> str:
        return InvoiceContent.timestamp_to_datetime(self._service_dict["date"]).strftime(
            "%d.%m.%Y"
        )

    @property
    def tariff_number(self) -> str:
        return "590"

    @property
    def code(self) -> str:
        return str(self._service_dict["code"])

    @property
    def session(self) -> str:
        return "1"

    @property
    def quantity(self) -> str:
        return "%.2f" % self._quantity

    @property
    def price(self) -> str:
        return "%.2f" % self._service_price

    @property
    def internal_scaling_factor(self) -> str:
        return "1.00"

    @property
    def tax_point_value(self) -> str:
        return "1.00"

    @property
    def provider_id(self) -> str:
        return "1"

    @property
    def responsible_id(self) -> str:
        return "2"

    @property
    def obligation(self) -> str:
        return "1"

    @property
    def vat_id(self) -> str:
        return "0"

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
