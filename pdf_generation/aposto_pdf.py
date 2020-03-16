from typing import Dict, List
from pathlib import Path
import json

from pdf_generation.text_style import TTFontToRegister, TextStyle
from pdf_generation.text import Text

from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
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

    def draw_string(self, left: float, top: float, text: str, style: TextStyle):
        x_mm: float = self.to_mm(left)
        y_mm: float = self.top_to_bottom(top)

        super().setFont(style.family, style.size)

        if style.align == "R":
            super().drawRightString(x_mm, y_mm, text)
        elif style.align == "C":
            super().drawCentredString(x_mm, y_mm, text)
        else:
            super().drawString(x_mm, y_mm, text)

    def to_mm(self, x: float) -> float:
        return x * mm

    def top_to_bottom(self, top: float) -> float:
        return self.to_mm(297 - top)

    def load_template(self, template_path: Path):
        with open(template_path.resolve().as_posix()) as json_template:
            self.template: List[Text] = list(
                Text.from_dict(text_dict) for text_dict in json.load(json_template)
            )
