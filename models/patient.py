from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, root_validator, validator
from typing_extensions import Literal


class Patient(BaseModel):
    """
    The patient who received the therapies
    """

    firstname: str = Field(
        title="First name",
        description="The patient first name",
        min_length=1,
        max_length=35,
    )

    lastname: str = Field(
        title="Last name",
        description="The patient last name",
        min_length=1,
        max_length=35,
    )

    street: str = Field(
        title="Street",
        description="The patient address street part. It contains the mailbox number and the street name. Extra information is not allowed",
        min_length=1,
        max_length=35,
    )

    zipcode: str = Field(
        title="zipcode", description="The patient zipcode code", min_length=1, max_length=9
    )

    city: str = Field(
        title="City", description="The patient city name", min_length=1, max_length=35
    )

    canton: Literal[
        "AG",
        "AI",
        "AR",
        "BE",
        "BL",
        "BS",
        "FR",
        "GE",
        "GL",
        "GR",
        "JU",
        "LU",
        "NE",
        "NW",
        "OW",
        "SG",
        "SH",
        "SO",
        "SZ",
        "TI",
        "TG",
        "UR",
        "VD",
        "VS",
        "ZG",
        "ZH",
        "LI",
        "A",
        "D",
        "F",
        "I",
    ] = Field(title="Canton", description="The patient Swiss canton")

    birthdate: datetime = Field(
        title="Birthday",
        description="The timestamp of the patient birthdate. The timestamp is expressed in milliseconds (JavaScript standard) except if negative (before 01/01/1970). If so, it is expressed in seconds",
    )

    gender: Literal["man", "woman"] = Field(
        title="Gender", description="The patient gender"
    )

    email: EmailStr = Field(
        title="Email",
        description="The patient email. Generated invoices can be sent to this email address",
    )

    @root_validator
    @classmethod
    def check_name(cls, values):
        first_name: str = values.get("firstname")
        last_name: str = values.get("lastname")

        if (
            first_name is not None
            and last_name is not None
            and len(f"{first_name} {last_name}") > 70
        ):
            raise ValueError("The therapist name is longer than 70 caracters.")

        return values
