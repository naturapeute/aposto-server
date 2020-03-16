from typing import List
from pathlib import Path
import json

from pdf_generation.text_style import TTFontToRegister, TextStyle
from pdf_generation.content import Text, Frame
from pdf_generation.template import DescriptorTemplate, FrameTemplate

from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT


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
        template: List[Text] = DescriptorTemplate(descriptor_template_path).load_template()

        for text in template:
            self.drawString(text)

    def draw_frame_template(self, frame_template_path: Path):
        template: List[Frame] = FrameTemplate(frame_template_path).load_template()

        for frame in template:
            self.draw_frame(frame)
