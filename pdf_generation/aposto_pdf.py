from pathlib import Path
from typing import List

from PIL import Image
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from pdf_generation.content import Graphic, Text, Value
from pdf_generation.invoice_content import InvoiceContent
from pdf_generation.template import (
    DescriptorTemplate,
    GraphicTemplate,
    ValueTemplate,
)
from pdf_generation.text_style import TextStyle, TTFontToRegister


class ApostoCanvas(canvas.Canvas):
    SERVICE_TOP_SHIFT: float = 6.363

    def __init__(self, filename: str):
        super().__init__(filename)
        self.register_fonts()

    def register_fonts(self):
        TTFontToRegister(Path("fonts/Arial.ttf"), "Arial").register()
        TTFontToRegister(Path("fonts/Arial Bold.ttf"), "Arial B").register()
        TTFontToRegister(Path("fonts/OCRB.ttf"), "ORCB").register()

    def setFont(self, style: TextStyle):
        return super().setFont(style.family, style.size)

    def drawString(self, text: Text):
        self.setFont(text.style)

        if text.style.align == "R":
            super().drawRightString(text.left, text.bottom, text.text)
        elif text.style.align == "C":
            super().drawCentredString(text.left, text.bottom, text.text)
        else:
            super().drawString(text.left, text.bottom, text.text)

    def draw_frame(self, frame: Graphic):
        self.rect(frame.left, frame.bottom, frame.width, frame.height, stroke=1)

    def draw_descriptor_template(self, descriptor_template_path: Path):
        template: List[Text] = DescriptorTemplate(
            descriptor_template_path
        ).load_template()

        for text in template:
            self.drawString(text)

    def draw_frame_template(self, frame_template_path: Path):
        self.setLineWidth(0.75)
        template: List[Graphic] = GraphicTemplate(frame_template_path).load_template()

        for frame in template:
            self.draw_frame(frame)

    def draw_value_template(
        self, value_template_path: Path, invoice_content: InvoiceContent
    ):
        template: List[Value] = ValueTemplate(value_template_path).load_template()

        if "services" not in value_template_path.as_posix():
            for value in template:
                self.drawString(value.to_text(invoice_content))
        else:
            for index, service in enumerate(invoice_content.services.services):
                for value in template:
                    text: Text = value.to_text(service)
                    text.shift_top(index * self.SERVICE_TOP_SHIFT)
                    self.drawString(text)

    def draw_datamatrix(
        self, datamatrix_template_path: Path, invoice_content: InvoiceContent
    ):
        datamatrix_image: Image = invoice_content.generate_datamatrix()

        if not datamatrix_image:
            return

        template: List[Graphic] = GraphicTemplate(
            datamatrix_template_path
        ).load_template()

        for datamatrix in template:
            self.drawImage(
                ImageReader(datamatrix_image),
                datamatrix.left,
                datamatrix.bottom,
                datamatrix.width,
                datamatrix.height,
            )

    def draw_scissors_template(self, scissors_template_path: Path):
        scissors_image: Image = Image.open("./pdf_generation/img/scissors.png")
        template: List[Graphic] = GraphicTemplate(scissors_template_path).load_template()

        for scissors in template:
            if scissors.rotate:
                scissors_image = scissors_image.rotate(scissors.rotate, expand=True)

            self.drawImage(
                ImageReader(scissors_image),
                scissors.left,
                scissors.bottom,
                width=scissors.width,
                height=scissors.height,
            )

    def draw_invoice(
        self,
        descriptor_template_paths: List[Path],
        frame_template_paths: List[Path],
        value_template_paths: List[Path],
        datamatrix_template_paths: List[Path],
        invoice_content: InvoiceContent,
    ):
        for descriptor_template_path in descriptor_template_paths:
            self.draw_descriptor_template(descriptor_template_path)

        for frame_template_path in frame_template_paths:
            self.draw_frame_template(frame_template_path)

        for value_template_path in value_template_paths:
            self.draw_value_template(value_template_path, invoice_content)

        for datamatrix_template_path in datamatrix_template_paths:
            self.draw_datamatrix(datamatrix_template_path, invoice_content)

        self.showPage()
