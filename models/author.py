from typing import Optional

from pydantic import BaseModel, EmailStr, constr


class Author(BaseModel):
    name: constr(min_length=1, max_length=70)
    street: constr(min_length=1, max_length=35)
    ZIP: constr(min_length=1, max_length=9)
    city: constr(min_length=1, max_length=35)
    phone: constr(strip_whitespace=True, min_length=1, max_length=25)
    email: EmailStr
    RCC: Optional[constr(regex=r"^[A-Z][0-9]{6}$")]
    QRIBAN: Optional[
        constr(strip_whitespace=True, regex=r"^CH[0-9]{2}3[0-1][0-9]{15}$")
    ] = None  # TODO : Turn into compulsory field when moving to QR-invoice
    ESRId: Optional[
        constr(strip_whitespace=True, regex=r"^[0-9]{6}$")
    ] = None  # TODO : Turn into compulsory field when moving to QR-invoice
    ESRBankId: Optional[
        constr(strip_whitespace=True, regex=r"^01[0-9]{7}$")
    ] = None  # TODO : Turn into compulsory field when moving to QR-invoice
