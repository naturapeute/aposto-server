from typing import List
from pathlib import Path
import json

from pdf_generation.text_style import TTFontToRegister, TextStyle
from pdf_generation.text import Text

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

    def load_template(self, template_path: Path):
        with open(template_path.resolve().as_posix()) as json_template:
            self.template: List[Text] = list(
                Text.from_dict(text_dict) for text_dict in json.load(json_template)
            )
