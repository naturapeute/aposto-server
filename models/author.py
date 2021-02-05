from typing import Optional

from pydantic import BaseModel, EmailStr, Field, validator
from pydantic.fields import ModelField


class Author(BaseModel):
    """
    The author who edits the invoice. It can be the therapy society or the therapist itself
    """

    name: str = Field(
        title="Name",
        description="The author name. It can be the therapy society name or the therapist's first name and last name",
        min_length=1,
        max_length=70,
    )

    street: str = Field(
        title="Street",
        description="The author address street part. It contains the mailbox number and the street name. Extra information is not allowed. All author address information corresponds to the address where the therapist performs therapies",
        min_length=1,
        max_length=35,
    )

    zipcode: str = Field(
        title="zipcode", description="The author zipcode code", min_length=1, max_length=9
    )

    city: str = Field(
        title="City", description="The author city name", min_length=1, max_length=35
    )

    phone: str = Field(
        title="Phone",
        description="The author phone number. It can be the therapy society phone number or the therapist phone number",
        min_length=1,
        max_length=25,
    )

    email: EmailStr = Field(
        title="Email",
        description="The author email. Generated invoices can be sent to this email address",
    )

    rcc: Optional[str] = Field(
        title="RCC",
        description="The author RCC number. It can be the therapy society RCC number or the therapist RCC number",
        regex=r"^[A-Z][0-9]{6}$",
    )

    iban: str = Field(
        title="IBAN",
        description="The author IBAN. The IBAN must correspond to the bank account that cashes invoices. It can be an IBAN or a QR-IBAN",
        regex=r"^CH(\d{2})(\d{5})([A-Z0-9]{12})$",
    )

    ESRId: Optional[str] = Field(
        None,
        title="ESR ID",
        description="The author ESR customer ID. It is provided by the bank institution (German: ESR, French: BVR, English: ISR)",
        regex=r"^[0-9]{6}$",
    )

    ESRBankId: Optional[str] = Field(
        None,
        title="ESR bank ID",
        description="The author ESR bank ID. It is provided by the bank institution (German: ESR, French: BVR, English: ISR)",
        regex=r"^01[0-9]{7}$",
    )

    @validator("phone", pre=True, allow_reuse=True)
    @classmethod
    def remove_phone_whitespace(cls, value: ModelField):
        return value.replace(" ", "")

    @validator("iban")
    @classmethod
    def check_iban_checksum(cls, value: ModelField):
        if str(98 - (int(f"{value[4:]}121700") % 97)) == value[2:4]:
            return value

        raise ValueError("IBAN checksum is invalid.")
