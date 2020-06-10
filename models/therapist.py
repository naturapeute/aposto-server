from typing import Optional

from pydantic import BaseModel, constr


class Therapist(BaseModel):
    firstName: constr(min_length=1, max_length=35)
    lastName: constr(min_length=1, max_length=35)
    street: constr(min_length=1, max_length=35)
    ZIP: constr(min_length=1, max_length=9)
    city: constr(min_length=1, max_length=35)
    phone: constr(strip_whitespace=True, min_length=1, max_length=25)
    RCC: Optional[constr(regex=r"^[A-Z][0-9]{6}$")]
