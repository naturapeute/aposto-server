from typing import Optional

from pydantic import BaseModel, EmailStr, constr


class Author(BaseModel):
    name: constr(max_length=70)
    street: constr(max_length=70)
    ZIP: constr(max_length=16)
    city: constr(max_length=35)
    phone: str
    email: EmailStr
    RCC: Optional[constr(regex=r"^[A-Z][0-9]{6}$")]
