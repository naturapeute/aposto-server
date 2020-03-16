from typing import Union
from pathlib import Path

from .text_style import TTFontToRegister, TextStyle

from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT


class ApostoCanvas(canvas.Canvas):
    def __init__(
        self, filename: str,
    ):
        super().__init__(filename)
        self.register_fonts()

    def register_fonts(self):
        TTFontToRegister(Path("fonts/Arial.ttf"), "Arial").register()
        TTFontToRegister(Path("fonts/Arial Bold.ttf"), "Arial B").register()
        TTFontToRegister(Path("fonts/OCRB.ttf"), "ORCB").register()

    def draw_string(self, x: float, y: float, text: str, style: TextStyle):
        x_mm: float = self.to_mm(x)
        y_mm: float = self.bottom_to_top(y)

        super().setFont(style.family, style.size)

        if style.align == "R":
            super().drawRightString(x_mm, y_mm, text)
        elif style.align == "C":
            super().drawCentredString(x_mm, y_mm, text)
        else:
            super().drawString(x_mm, y_mm, text)

    def to_mm(self, x: float) -> float:
        return x * mm

    def bottom_to_top(self, y: float) -> float:
        return self.to_mm(297 - y)
