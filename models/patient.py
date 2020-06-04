from datetime import datetime

from pydantic import BaseModel, EmailStr, constr, root_validator
from typing_extensions import Literal


class Patient(BaseModel):
    firstName: str
    lastName: str
    street: constr(max_length=70)
    ZIP: constr(max_length=16)
    city: constr(max_length=35)
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
    ]
    birthday: datetime
    gender: Literal["male", "female"]
    email: EmailStr

    @root_validator
    @classmethod
    def check_name(cls, values):
        first_name: str = values.get("firstName")
        last_name: str = values.get("lastName")

        if (
            first_name is not None
            and last_name is not None
            and len(f"{first_name} {last_name}") > 70
        ):
            raise ValueError(f"The therapist name is longer than 70 caracters.")

        return values
