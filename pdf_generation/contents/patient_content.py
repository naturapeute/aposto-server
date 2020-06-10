from models.patient import Patient


class PatientContent:
    def __init__(self, patient: Patient):
        self._patient: Patient = patient

    @property
    def first_name(self) -> str:
        return self._patient.firstName

    @property
    def last_name(self) -> str:
        return self._patient.lastName

    @property
    def street(self) -> str:
        return self._patient.street

    @property
    def zip(self) -> str:
        return self._patient.ZIP

    @property
    def city(self) -> str:
        return self._patient.city

    @property
    def birthday(self) -> str:
        return self._patient.birthday.strftime("%d.%m.%Y")

    @property
    def gender(self) -> str:
        if self._patient.gender == "male":
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
    def birthday_with_header_and_gender(self) -> str:
        return f"Date de naissance {self.birthday}/{self.gender}"

    @property
    def ssn(self) -> str:
        # NOTE : SSN is optional in Tarif 590 documentation. However, it is
        # used in the optional datamatrix code. So if the datamatrix code is
        # generated, we juste leave the SSN empty.
        return ""
