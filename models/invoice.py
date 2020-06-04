from datetime import datetime
from typing import Optional

from pydantic import BaseModel, conint, conlist

from models.author import Author
from models.patient import Patient
from models.service import Service
from models.therapist import Therapist


class Invoice(BaseModel):
    terrapeuteID: Optional[int] = None
    author: Author
    therapist: Therapist
    patient: Patient
    servicePrice: conint(gt=0)
    services: conlist(Service, min_items=1)
    timestamp: datetime
