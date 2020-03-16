from typing import Dict
from collections import namedtuple

import pdf_generation
from pdf_generation.text_style import TextStyle

from reportlab.lib.units import mm


class Text:
    def __init__(self, dict_text: Dict):
        self.text: str = dict_text["text"]
        self._left: float = dict_text["left"]
        self._top: float = dict_text["top"]
        self.style: TextStyle = getattr(pdf_generation.text_style, dict_text["style"])()

    @property
    def left(self):
        return Text.to_mm(self._left)

    @property
    def bottom(self):
        return Text.top_to_bottom(self._top)

    @staticmethod
    def to_mm(x: float) -> float:
        return x * mm

    @staticmethod
    def top_to_bottom(top: float) -> float:
        return Text.to_mm(297 - top)
