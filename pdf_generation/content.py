from functools import reduce
from typing import Dict, Union

from PIL import Image
from reportlab.lib.units import mm

import pdf_generation
from pdf_generation.invoice_content import InvoiceContent, Service
from pdf_generation.text_style import TextStyle


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
    def to_mm(val: float) -> float:
        return val * mm

    @staticmethod
    def top_to_bottom(top: float) -> float:
        return Content.to_mm(297 - top)


class Text(Content):
    def __init__(self, dict_text: Dict):
        super().__init__(dict_text)
        self.text: str = dict_text["text"]
        self.style: TextStyle = getattr(pdf_generation.text_style, dict_text["style"])()

    def shift_top(self, shift: float):
        self._top += shift


class Graphic(Content):
    def __init__(self, dict_frame: Dict):
        super().__init__(dict_frame)
        self._width: float = dict_frame["width"]
        self._height: float = dict_frame["height"]
        self._rotate: float = dict_frame["rotate"] if "rotate" in dict_frame else None

    @property
    def width(self):
        return self.to_mm(self._width)

    @property
    def height(self):
        return self.to_mm(self._height)

    @property
    def rotate(self):
        return self._rotate


class Value(Content):
    def __init__(self, dict_value: Dict):
        super().__init__(dict_value)
        self.key: str = dict_value["key"]
        self.style: TextStyle = getattr(pdf_generation.text_style, dict_value["style"])()

    def to_text(self, content: Union[InvoiceContent, Service]) -> Text:
        return Text(
            {
                "text": reduce(getattr, self.key.split("."), content),
                "left": self._left,
                "top": self._top,
                "style": type(self.style).__name__,
            }
        )


class Datamatrix(Content):
    def __init__(self, image: Image):
        super().__init__({"left": 15.817, "top": 276.856})
        self.image: Image = image
        self.dim: float = 16.462 * mm
