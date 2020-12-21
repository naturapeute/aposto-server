from typing import Optional

from pydantic import BaseModel, Field, validator
from pydantic.fields import ModelField


class Therapist(BaseModel):
    """
    The therapist who performed the billed therapies
    """

    firstname: str = Field(
        title="First name",
        description="The therapist first name",
        min_length=1,
        max_length=35,
    )

    lastname: str = Field(
        title="Last name",
        description="The therapist last name",
        min_length=1,
        max_length=35,
    )

    street: str = Field(
        title="Street",
        description="The therapist address street part. It contains the mailbox number and the street name. Extra information is not allowed",
        min_length=1,
        max_length=35,
    )

    zipcode: str = Field(
        title="zipcode", description="The therapist zipcode code", min_length=1, max_length=9,
    )

    city: str = Field(
        title="City", description="The therapist city name", min_length=1, max_length=35
    )

    phone: str = Field(
        title="Phone",
        description="The therapist phone number",
        min_length=1,
        max_length=25,
    )

    rcc: Optional[str] = Field(
        title="RCC", description="The therapist RCC number", regex=r"^[A-Z][0-9]{6}$",
    )

    @validator("phone", pre=True, allow_reuse=True)
    @classmethod
    def remove_phone_whitespace(cls, value: ModelField):
        return value.replace(" ", "")
