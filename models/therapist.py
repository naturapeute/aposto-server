from typing import Optional

from pydantic import BaseModel, constr


class Therapist(BaseModel):
    firstName: str
    lastName: str
    street: str
    ZIP: str
    city: str
    phone: str
    RCC: Optional[constr(regex=r"^[A-Z][0-9]{6}$")]
