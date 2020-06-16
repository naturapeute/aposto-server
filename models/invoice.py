from datetime import datetime
from typing import List, Optional, Tuple

from pydantic import BaseModel, Field, validator
from pydantic.fields import ModelField

from .author import Author
from .patient import Patient
from .service import Service
from .therapist import Therapist


class Invoice(BaseModel):
    """
    The `Invoice` model gathers all the information required for generating an invoice with Aposto,
    based on Tarif 590 and QR-invoice Swiss standards
    """

    naturapeuteID: Optional[str] = Field(
        None,
        title="Naturapeute ID",
        description="The Naturapeute user ID",
        regex=r"^[a-fA-F0-9]{24}$",
    )

    author: Author = Field(
        title="Author",
        description="The invoice author. It can be the therapy society or the therapist itself",
    )

    therapist: Therapist = Field(
        title="Therapist", description="The therapist who performed the treatment"
    )

    patient: Patient = Field(
        title="Patient", description="The patient who received the treatment"
    )

    servicePrice: int = Field(
        title="Service price", description="The hourly price the therapist charges", gt=0
    )

    services: List[Service] = Field(
        title="Services",
        description="The list of services performed as part of the treatment",
        min_items=1,
        max_items=5,
    )

    QRReference: Optional[str] = Field(
        None,
        title="QR-reference",
        description="The invoice QR-reference",
        regex=r"^[0-9]{27}$",
    )  # TODO : Turn into compulsory field when moving to QR-invoice

    timestamp: datetime = Field(
        title="Timestamp",
        description="The timestamp of the date the treatment was performed. The timestamp is expressed in milliseconds (JavaScript standard) except if negative (before 01/01/1970). If so, it is expressed in seconds",
    )

    # FIXME : pydantic actually does not support JavaScript negative timestamp
    #           Remove this code when it will be properly parsed.
    #           See https://github.com/samuelcolvin/pydantic/issues/1600
    @validator("timestamp", pre=True)
    @classmethod
    def check_valid_pydantic_date(cls, value: ModelField):
        if value < -int(2e10):
            raise ValueError(f"Negative timestamps bigger than {2e10} are not allowed.")

        return value

    @property
    def total_amount(self) -> float:
        _total_amount: float = 0.0

        for service in self.services:
            _total_amount += service.amount(self.servicePrice / 12)

        return _total_amount

    @property
    def therapy_dates(self) -> Tuple[datetime, datetime]:
        services_dates: List[datetime] = list(service.date for service in self.services)

        return (min(services_dates), max(services_dates))
