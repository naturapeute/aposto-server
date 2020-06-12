from pathlib import Path

from .aposto_pdf import ApostoCanvas
from .contents import InvoiceContent
from .invoice_templates import (
    invoice_datamatrix_template,
    invoice_descriptor_templates,
    invoice_frame_template,
    invoice_services_template,
    invoice_value_templates,
)
from .qr_invoice_templates import (
    qr_invoice_descriptor_templates,
    qr_invoice_qr_part_descriptor_templates,
    qr_invoice_frame_template,
    qr_invoice_scissors_template,
    qr_invoice_swiss_qr_code_template,
    qr_invoice_value_templates,
    qr_invoice_qr_part_value_templates,
    qr_invoice_qr_part_frame_template,
)


class PDFGenerator:
    def __init__(self, invoice_content: InvoiceContent):
        self._invoice_content: InvoiceContent = invoice_content

    @property
    def invoice_path(self) -> Path:
        invoice_dir_str = (
            f"./out/{self._invoice_content.naturapeute_id}"
            if self._invoice_content.naturapeute_id
            else "./out/demo"
        )
        invoice_dir: Path = Path(invoice_dir_str)
        invoice_dir.mkdir(parents=True, exist_ok=True)

        return invoice_dir.joinpath(f"invoice-{self._invoice_content.timestamp}.pdf")

    def generate_invoice(self) -> Path:
        invoice_path: Path = self.invoice_path

        if not invoice_path.exists():
            cvs: ApostoCanvas = ApostoCanvas(invoice_path.as_posix())

            # QR-invoice page
            for qr_invoice_descriptor_template in qr_invoice_descriptor_templates:
                cvs.draw_descriptor_template(qr_invoice_descriptor_template)

            cvs.draw_frame_template(qr_invoice_frame_template)

            for qr_invoice_value_template in qr_invoice_value_templates:
                cvs.draw_value_template(qr_invoice_value_template, self._invoice_content)

            if (
                self._invoice_content.qr_reference
                and self._invoice_content.author.qr_iban
            ):
                # QR-invoice part in QR-invoice page
                for (
                    qr_invoice_qr_part_descriptor_template
                ) in qr_invoice_qr_part_descriptor_templates:
                    cvs.draw_descriptor_template(qr_invoice_qr_part_descriptor_template)

                for (
                    qr_invoice_qr_part_value_template
                ) in qr_invoice_qr_part_value_templates:
                    cvs.draw_value_template(
                        qr_invoice_qr_part_value_template, self._invoice_content
                    )

                cvs.draw_frame_template(qr_invoice_qr_part_frame_template)
                cvs.draw_scissors_template(qr_invoice_scissors_template)
                cvs.draw_swiss_qr_code_template(
                    qr_invoice_swiss_qr_code_template, self._invoice_content
                )

            cvs.showPage()

            # Invoice page
            for invoice_descriptor_template in invoice_descriptor_templates:
                cvs.draw_descriptor_template(invoice_descriptor_template)

            cvs.draw_frame_template(invoice_frame_template)

            for invoice_value_template in invoice_value_templates:
                cvs.draw_value_template(invoice_value_template, self._invoice_content)

            cvs.draw_value_template(
                invoice_services_template, self._invoice_content, is_service_template=True
            )

            cvs.draw_datamatrix_template(
                invoice_datamatrix_template, self._invoice_content
            )

            cvs.showPage()

            cvs.save()

        return invoice_path
