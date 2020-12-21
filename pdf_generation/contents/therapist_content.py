from models import Therapist
from .entity_content import EntityContent


class TherapistContent(EntityContent):
    def __init__(self, therapist: Therapist):
        super().__init__(therapist)
        self._therapist: Therapist = therapist

    @property
    def name(self) -> str:
        return f"{self._therapist.firstname} {self._therapist.lastname}"
