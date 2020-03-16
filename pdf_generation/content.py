from typing import Dict
from collections import namedtuple

import pdf_generation
from pdf_generation.text_style import TextStyle

from reportlab.lib.units import mm


class Content:
    def __init__(self, dict_content: Dict):
        self._left: float = dict_content["left"]
        self._top: float = dict_content["top"]

    @property
    def left(self):
        return Content.to_mm(self._left)

    @property
    def bottom(self):
        return Content.top_to_bottom(self._top)

    @staticmethod
    def to_mm(x: float) -> float:
        return x * mm

    @staticmethod
    def top_to_bottom(top: float) -> float:
        return Content.to_mm(297 - top)


class Text(Content):
    def __init__(self, dict_text: Dict):
        super().__init__(dict_text)
        self.text: str = dict_text["text"]
        self.style: TextStyle = getattr(pdf_generation.text_style, dict_text["style"])()


class Frame(Content):
    def __init__(self, dict_frame: Dict):
        super().__init__(dict_frame)
        self._width: float = dict_frame["width"]
        self._height: float = dict_frame["height"]

    @property
    def width(self):
        return self.to_mm(self._width)

    @property
    def height(self):
        return self.to_mm(self._height)
