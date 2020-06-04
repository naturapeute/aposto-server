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
    QRIBAN: Optional[
        constr(strip_whitespace=True, regex=r"^CH[0-9]{2}3[0-1][0-9]{15}$")
    ] = None  # TODO : Turn into compulsory field when moving to QR-invoice
    ESRId: Optional[
        constr(strip_whitespace=True, regex=r"^[0-9]{6}$")
    ] = None  # TODO : Turn into compulsory field when moving to QR-invoice
    ESRBankId: Optional[
        constr(strip_whitespace=True, regex=r"^01[0-9]{7}$")
    ] = None  # TODO : Turn into compulsory field when moving to QR-invoice
