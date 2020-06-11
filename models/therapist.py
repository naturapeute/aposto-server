from typing import Optional

from pydantic import BaseModel, Field, validator
from pydantic.fields import ModelField


class Therapist(BaseModel):
    """
    The therapist who performed the billed therapies
    """

    firstName: str = Field(
        title="First name",
        description="The therapist first name",
        min_length=1,
        max_length=35,
    )

    lastName: str = Field(
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

    ZIP: str = Field(
        title="ZIP", description="The therapist ZIP code", min_length=1, max_length=9,
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

    RCC: Optional[str] = Field(
        title="RCC", description="The therapist RCC number", regex=r"^[A-Z][0-9]{6}$",
    )

    @validator("phone", pre=True)
    @classmethod
    def remove_phone_whitespace(cls, value: ModelField):
        return value.replace(" ", "")
