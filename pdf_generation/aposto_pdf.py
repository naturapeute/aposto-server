from typing import List, Dict
from pathlib import Path
import json

from pdf_generation.text_style import TTFontToRegister, TextStyle
from pdf_generation.content import Text, Frame, Value, Datamatrix
from pdf_generation.template import DescriptorTemplate, FrameTemplate, ValueTemplate
from pdf_generation.receipt_content import ReceiptContent

from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.utils import ImageReader


class ApostoCanvas(canvas.Canvas):
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

    def draw_frame(self, frame: Frame):
        self.rect(frame.left, frame.bottom, frame.width, frame.height, stroke=1)

    def draw_descriptor_template(self, descriptor_template_path: Path):
        template: List[Text] = DescriptorTemplate(
            descriptor_template_path
        ).load_template()

        for text in template:
            self.drawString(text)

    def draw_frame_template(self, frame_template_path: Path):
        template: List[Frame] = FrameTemplate(frame_template_path).load_template()

        for frame in template:
            self.draw_frame(frame)

    def draw_value_template(
        self, value_template_path: Path, receipt_content: ReceiptContent
    ):
        template: List[Value] = ValueTemplate(value_template_path).load_template()

        if "services" not in value_template_path.as_posix():
            for value in template:
                self.drawString(value.to_text(receipt_content))
        else:
            SERVICE_TOP_SHIFT: float = 6.363

            for index, service in enumerate(receipt_content.services.services):
                for value in template:
                    text: Text = value.to_text(service)
                    text.shift_top(index * SERVICE_TOP_SHIFT)
                    self.drawString(text)

    def draw_datamatrix(self, receipt_content: ReceiptContent):
        datamatrix: Datamatrix = Datamatrix(receipt_content.generate_datamatrix())
        self.drawImage(
            ImageReader(datamatrix.image),
            datamatrix.left,
            datamatrix.bottom,
            width=datamatrix.dim,
            height=datamatrix.dim,
        )

    def draw_full_receipt(
        self,
        descriptor_template_paths: List[Path],
        frame_template_paths: List[Path],
        value_template_paths: List[Path],
        receipt_content: ReceiptContent,
    ):
        for descriptor_template_path in descriptor_template_paths:
            self.draw_descriptor_template(descriptor_template_path)

        for frame_template_path in frame_template_paths:
            self.draw_frame_template(frame_template_path)

        for value_template_path in value_template_paths:
            self.draw_value_template(value_template_path, receipt_content)

        self.draw_datamatrix(receipt_content)
