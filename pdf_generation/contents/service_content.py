from models.service import Service
from pdf_generation.service_codes import SERVICE_CODES


class ServiceContent:
    def __init__(self, service: Service, service_unit_price: float):
        self._service: Service = service
        self._service_unit_price: float = service_unit_price

    @property
    def date(self) -> str:
        return self._service.date.strftime("%d.%m.%Y")

    @property
    def tariff_number(self) -> str:
        return "590"

    @property
    def code(self) -> str:
        return str(self._service.code)

    @property
    def session(self) -> str:
        return "1"

    @property
    def quantity(self) -> str:
        return "%.2f" % self._service.quantity

    @property
    def price(self) -> str:
        return "%.2f" % self._service_unit_price

    @property
    def internal_scaling_factor(self) -> str:
        return "1.00"

    @property
    def tax_point_value(self) -> str:
        return "1.00"

    @property
    def provider_id(self) -> str:
        return "1"

    @property
    def responsible_id(self) -> str:
        return "2"

    @property
    def obligation(self) -> str:
        return "1"

    @property
    def vat_id(self) -> str:
        return "0"

    @property
    def amount(self) -> str:
        return "%.2f" % self._service.amount(self._service_unit_price)

    @property
    def code_label(self) -> str:
        return next(
            service_code["label"]
            for service_code in SERVICE_CODES
            if service_code["value"] == self._service.code
        )
