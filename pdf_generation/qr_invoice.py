import qrcode
from PIL import Image
from qrcode import QRCode

from .contents import InvoiceContent


class QRInvoice:
    def __init__(self, invoice_content: InvoiceContent):
        self.invoice_content: InvoiceContent = invoice_content

    @property
    def separator(self) -> str:
        return "\r\n"

    @property
    def header_qr_type(self) -> str:
        return "SPC"

    @property
    def header_version(self) -> str:
        return "0210"

    @property
    def header_coding(self) -> str:
        return "1"

    @property
    def header(self) -> str:
        return f"{self.header_qr_type}{self.separator}{self.header_version}{self.separator}{self.header_coding}"

    @property
    def cdtr_inf_iban(self) -> str:
        return self.invoice_content.author_content.iban

    @property
    def cdtr_inf(self) -> str:
        return self.cdtr_inf_iban

    @property
    def cdtr_adr_tp(self) -> str:
        return "K"

    @property
    def cdtr_name(self) -> str:
        return self.invoice_content.author_content.name

    @property
    def cdtr_strt_nm_or_adr_line1(self) -> str:
        return self.invoice_content.author_content.street

    @property
    def cdtr_bldg_nb_or_adr_line2(self) -> str:
        return self.invoice_content.author_content.zip_city

    @property
    def cdtr_pst_cd(self) -> str:
        return ""

    @property
    def cdtr_twn_nm(self) -> str:
        return ""

    @property
    def cdtr_ctry(self) -> str:
        return "CH"

    @property
    def cdtr(self) -> str:
        _cdtr: str = self.cdtr_adr_tp
        _cdtr: str = f"{_cdtr}{self.separator}{self.cdtr_name}"
        _cdtr: str = f"{_cdtr}{self.separator}{self.cdtr_strt_nm_or_adr_line1}"
        _cdtr: str = f"{_cdtr}{self.separator}{self.cdtr_bldg_nb_or_adr_line2}"
        _cdtr: str = f"{_cdtr}{self.separator}{self.cdtr_pst_cd}"
        _cdtr: str = f"{_cdtr}{self.separator}{self.cdtr_twn_nm}"
        _cdtr: str = f"{_cdtr}{self.separator}{self.cdtr_ctry}"

        return _cdtr

    @property
    def ccy_amt_amt(self) -> str:
        return self.invoice_content.total_amount

    @property
    def ccy_amt_ccy(self) -> str:
        return "CHF"

    @property
    def ccy_amt(self) -> str:
        return f"{self.ccy_amt_amt}{self.separator}{self.ccy_amt_ccy}"

    @property
    def ultmt_dbtr_adr_tp(self) -> str:
        return "K"

    @property
    def ultmt_dbtr_name(self) -> str:
        return self.invoice_content.patient_content.name

    @property
    def ultmt_dbtr_strt_nm_or_adr_line1(self) -> str:
        return self.invoice_content.patient_content.street

    @property
    def ultmt_dbtr_bldg_nb_or_adr_line2(self) -> str:
        return self.invoice_content.patient_content.zip_city

    @property
    def ultmt_dbtr_pst_cd(self) -> str:
        return ""

    @property
    def ultmt_dbtr_twn_nm(self) -> str:
        return ""

    @property
    def ultmt_dbtr_ctry(self) -> str:
        return "CH"

    @property
    def ultmt_dbtr(self) -> str:
        _ultmt_dbtr: str = self.ultmt_dbtr_adr_tp
        _ultmt_dbtr: str = f"{_ultmt_dbtr}{self.separator}{self.ultmt_dbtr_name}"
        _ultmt_dbtr: str = f"{_ultmt_dbtr}{self.separator}{self.ultmt_dbtr_strt_nm_or_adr_line1}"
        _ultmt_dbtr: str = f"{_ultmt_dbtr}{self.separator}{self.ultmt_dbtr_bldg_nb_or_adr_line2}"
        _ultmt_dbtr: str = f"{_ultmt_dbtr}{self.separator}{self.ultmt_dbtr_pst_cd}"
        _ultmt_dbtr: str = f"{_ultmt_dbtr}{self.separator}{self.ultmt_dbtr_twn_nm}"
        _ultmt_dbtr: str = f"{_ultmt_dbtr}{self.separator}{self.ultmt_dbtr_ctry}"

        return _ultmt_dbtr

    @property
    def rmt_inf_tp(self) -> str:
        return "QRR"

    @property
    def rmt_inf_ref(self) -> str:
        return self.invoice_content.reference

    @property
    def rmt_inf(self) -> str:
        return f"{self.rmt_inf_tp}{self.separator}{self.rmt_inf_ref}"

    @property
    def add_inf_ustrd(self) -> str:
        return ""

    @property
    def add_inf_trailer(self) -> str:
        return "EPD"

    @property
    def add_inf_strd_bkg_inf(self) -> str:
        return ""

    @property
    def add_inf(self) -> str:
        return f"{self.add_inf_ustrd}{self.separator}{self.add_inf_trailer}{self.separator}{self.add_inf_strd_bkg_inf}"

    def _generate_qr_code_string(self) -> str:
        qr_code_string: str = f"{self.header}"
        qr_code_string: str = f"{qr_code_string}{self.separator}{self.cdtr_inf}"
        qr_code_string: str = f"{qr_code_string}{self.separator}{self.cdtr}"
        qr_code_string: str = f"{qr_code_string}{self.separator}{self.ccy_amt}"
        qr_code_string: str = f"{qr_code_string}{self.separator}{self.ultmt_dbtr}"
        qr_code_string: str = f"{qr_code_string}{self.separator}{self.rmt_inf}"
        qr_code_string: str = f"{qr_code_string}{self.separator}{self.add_inf}"

        return qr_code_string

    def generate_qr_code(self) -> Image.Image:
        qr_code_string: str = self._generate_qr_code_string()

        qr_code: QRCode = QRCode(
            version=10, error_correction=qrcode.constants.ERROR_CORRECT_M, border=0,
        )
        qr_code.add_data(qr_code_string)
        qr_code.make()

        return qr_code.make_image().get_image()
