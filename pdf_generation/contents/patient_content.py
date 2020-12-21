from models import Patient


class PatientContent:
    def __init__(self, patient: Patient):
        self._patient: Patient = patient

    @property
    def first_name(self) -> str:
        return self._patient.firstname

    @property
    def last_name(self) -> str:
        return self._patient.lastname

    @property
    def street(self) -> str:
        return self._patient.street

    @property
    def zip(self) -> str:
        return self._patient.zipcode

    @property
    def city(self) -> str:
        return self._patient.city

    @property
    def birthdate(self) -> str:
        return self._patient.birthdate.strftime("%d.%m.%Y")

    @property
    def gender(self) -> str:
        if self._patient.gender == "man":
            return "H"
        else:
            return "F"

    @property
    def canton(self) -> str:
        return self._patient.canton

    @property
    def name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def zip_city(self) -> str:
        return f"{self.zip} {self.city}"

    @property
    def email(self) -> str:
        return self._patient.email

    @property
    def birthdate_with_header_and_gender(self) -> str:
        return f"Date de naissance {self.birthdate}/{self.gender}"

    @property
    def ssn(self) -> str:
        # NOTE : SSN is optional in Tarif 590 documentation. However, it is
        # used in the optional datamatrix code. So if the datamatrix code is
        # generated, we juste leave the SSN empty.
        return ""
