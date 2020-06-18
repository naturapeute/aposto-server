from typing import List, Union

from dateutil import tz
from PIL import Image
from pystrich.datamatrix import DataMatrixEncoder, DataMatrixRenderer

from models import Invoice
from .author_content import AuthorContent
from .patient_content import PatientContent
from .service_content import ServiceContent
from .therapist_content import TherapistContent


class InvoiceContent:
    def __init__(self, invoice: Invoice):
        self._invoice: Invoice = invoice

        self.author_content: AuthorContent = AuthorContent(self._invoice.author)
        self.therapist_content: TherapistContent = TherapistContent(
            self._invoice.therapist
        )
        self.patient_content: PatientContent = PatientContent(self._invoice.patient)
        self.services_content: List[ServiceContent] = list(
            ServiceContent(service, self._invoice.servicePrice / 12)
            for service in self._invoice.services
        )

    @property
    def naturapeute_id(self) -> Union[str, None]:
        return self._invoice.naturapeuteID

    @property
    def timestamp(self) -> str:
        return str(int(self._invoice.timestamp.timestamp() * 1000))[:-3]

    @property
    def full_date_string(self) -> str:
        return self._invoice.timestamp.astimezone(tz.gettz("Europe/Zurich")).strftime(
            "%d.%m.%Y %H:%M:%S"
        )

    @property
    def date_string(self) -> str:
        return self._invoice.timestamp.astimezone(tz.gettz("Europe/Zurich")).strftime(
            "%d.%m.%Y"
        )

    @property
    def identification(self) -> str:
        return f"{self.timestamp} · {self.full_date_string}"

    @property
    def page(self) -> str:
        return str(1)

    @property
    def therapy_dates(self) -> str:
        (therapy_start_date, therapy_end_date) = self._invoice.therapy_dates

        return f"{therapy_start_date.astimezone(tz.gettz('Europe/Zurich')).strftime('%d.%m.%Y')} - {therapy_end_date.astimezone(tz.gettz('Europe/Zurich')).strftime('%d.%m.%Y')}"

    @property
    def therapy_reason(self) -> str:
        return "Maladie"

    @property
    def invoice_number_and_date(self) -> str:
        return f"{self.date_string} / {self.timestamp}"

    @property
    def gln_list(self) -> str:
        return f"1/{self.author_content.gln} 2/{self.therapist_content.gln}"

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
        return "%.2f" % self._invoice.total_amount

    @property
    def paid_amount(self) -> str:
        return self.total_amount if self._invoice.paid else "0.00"

    @property
    def owed_amount(self) -> str:
        return "0.00" if self._invoice.paid else self.total_amount

    @property
    def reference_type(self) -> str:
        return self._invoice.reference_type

    @property
    def reference(self) -> str:
        reference: str = self._invoice.reference

        if self._invoice.reference_type == "SCOR":
            reference: str = " ".join(
                [reference[i : i + 4] for i in range(0, len(reference), 4)]
            )
        elif self._invoice.reference_type == "QRR":
            reference: str = " ".join(
                [reference[0:2]]
                + [reference[i : i + 5] for i in range(2, len(reference), 5)]
            )

        return reference

    @property
    def esr_coding_line(self) -> Union[str, None]:
        if not self._invoice.author.ESRId or not self._invoice.author.ESRBankId:
            return None

        total_amount: str = self.total_amount.replace(".", "").rjust(10, "0")

        return f"01{total_amount}>{self._invoice.author.ESRId}{self._invoice.QRReference}+ {self._invoice.author.ESRBankId}"

    def _generate_datamatrix_string(self) -> Union[str, None]:
        if not self.esr_coding_line:
            return None

        separator: str = "#"
        therapy_start_date = (
            self._invoice.therapy_dates[0]
            .astimezone(tz.gettz("Europe/Zurich"))
            .strftime("%d.%m.%Y")
        )
        due_amount: str = "0"

        datamatrix_string = f"{self.esr_coding_line}{separator}{self.author_content.gln}{separator}{self.therapist_content.gln}{separator}"
        datamatrix_string = f"{datamatrix_string}{therapy_start_date}{separator}{self.patient_content.ssn}{separator}{self.patient_content.birthday}{separator}"
        datamatrix_string = f"{datamatrix_string}{due_amount}{separator}"

        for service in self.services_content:
            datamatrix_string = (
                f"{datamatrix_string}{int(service.float_amount) % 10}{separator}"
            )

        if len(datamatrix_string) > 169:
            datamatrix_string = datamatrix_string[-169:]
        elif len(datamatrix_string) < 169:
            datamatrix_string = datamatrix_string.ljust(169, "0")

        return datamatrix_string

    def generate_datamatrix(self) -> Union[Image.Image, None]:
        # NOTE : For now, the ESR identification and ESR bank identification is never provided. So
        #           the datamatrix_string is always None and never generated.
        #
        #           It seems that it is not needed for QR-invoice as it replaces ESR invoice (in
        #           french BVR).
        datamatrix_string: str = self._generate_datamatrix_string()

        if not datamatrix_string:
            return None

        encoder: DataMatrixEncoder = DataMatrixEncoder(datamatrix_string)
        renderer: DataMatrixRenderer = DataMatrixRenderer(encoder.matrix, encoder.regions)

        return renderer.get_pilimage(10)
