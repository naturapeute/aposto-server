from pathlib import Path
from typing import List

from PIL import Image
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from .content import Graphic, SwissQRCode, Text, Value
from .contents import InvoiceContent
from .qr_invoice import QRInvoice
from .text_style import TextStyle, TTFontToRegister


class ApostoCanvas(canvas.Canvas):
    SERVICE_TOP_SHIFT: float = 6.363

    def __init__(self, filename: str):
        super().__init__(filename)
        self._register_fonts()

    def _register_fonts(self):
        TTFontToRegister(Path("fonts/Arial.ttf"), "Arial").register()
        TTFontToRegister(Path("fonts/Arial Bold.ttf"), "Arial B").register()
        TTFontToRegister(Path("fonts/OCRB.ttf"), "ORCB").register()

    def _set_font(self, style: TextStyle):
        return super().setFont(style.family, style.size)

    def _draw_string(self, text: Text):
        self._set_font(text.style)

        if text.style.align == "R":
            super().drawRightString(text.left, text.bottom, text.text)
        elif text.style.align == "C":
            super().drawCentredString(text.left, text.bottom, text.text)
        else:
            super().drawString(text.left, text.bottom, text.text)

    def _draw_frame(self, frame: Graphic):
        super().rect(frame.left, frame.bottom, frame.width, frame.height, stroke=1)

    def _draw_image(self, image: Image.Image, graphic: Graphic):
        super().drawImage(
            ImageReader(image),
            graphic.left,
            graphic.bottom,
            graphic.width,
            graphic.height,
        )

    def draw_descriptor_template(self, descriptor_template: List[Text]):
        for descriptor in descriptor_template:
            self._draw_string(descriptor)

    def draw_frame_template(self, frame_template: List[Graphic]):
        super().setLineWidth(0.75)

        for frame in frame_template:
            self._draw_frame(frame)

    def draw_value_template(
        self,
        value_template: List[Value],
        invoice_content: InvoiceContent,
        is_service_template: bool = False,
    ):
        if not is_service_template:
            for value in value_template:
                self._draw_string(value.to_text(invoice_content))
        else:
            for index, service_content in enumerate(invoice_content.services_content):
                for value in value_template:
                    text: Text = value.to_text(service_content)
                    text.shift_top(index * self.SERVICE_TOP_SHIFT)
                    self._draw_string(text)

    def draw_datamatrix_template(
        self, datamatrix_template: List[Graphic], invoice_content: InvoiceContent
    ):
        datamatrix_image: Image.Image = invoice_content.generate_datamatrix()

        if not datamatrix_image:
            return

        for datamatrix in datamatrix_template:
            self._draw_image(datamatrix_image, datamatrix)

    def draw_scissors_template(self, scissors_template: List[Graphic]):
        scissors_image: Image = Image.open("./pdf_generation/img/scissors.png")

        for scissors in scissors_template:
            if scissors.rotate:
                scissors_image = scissors_image.rotate(scissors.rotate, expand=True)

            self._draw_image(scissors_image, scissors)

    def draw_swiss_qr_code_template(
        self, swiss_qr_code_template: List[SwissQRCode], invoice_content: InvoiceContent
    ):
        qr_code_image: Image.Image = QRInvoice(invoice_content).generate_qr_code()
        swiss_cross_image: Image.Image = Image.open(
            "./pdf_generation/img/swiss_cross.png"
        )

        for swiss_qr_code in swiss_qr_code_template:
            self._draw_image(qr_code_image, swiss_qr_code.qr_code)
            self._draw_image(swiss_cross_image, swiss_qr_code.swiss_cross)
