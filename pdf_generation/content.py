from functools import reduce
from typing import Union

from reportlab.lib.units import mm

import pdf_generation
from pdf_generation.contents.invoice_content import InvoiceContent
from pdf_generation.contents.service_content import ServiceContent
from pdf_generation.text_style import TextStyle


class Content:
    def __init__(self, dict_content: dict):
        self._left: float = dict_content["left"]
        self._top: float = dict_content["top"]

    @property
    def left(self) -> float:
        return Content.to_mm(self._left)

    @property
    def bottom(self) -> float:
        return Content.top_to_bottom(self._top)

    @staticmethod
    def to_mm(val: float) -> float:
        return val * mm

    @staticmethod
    def top_to_bottom(top: float) -> float:
        return Content.to_mm(297 - top)


class Text(Content):
    def __init__(self, dict_text: dict):
        super().__init__(dict_text)
        self.text: str = dict_text["text"]
        self.style: TextStyle = getattr(pdf_generation.text_style, dict_text["style"])()

    def shift_top(self, shift: float):
        self._top += shift


class Graphic(Content):
    def __init__(self, dict_frame: dict):
        super().__init__(dict_frame)
        self._width: float = dict_frame["width"]
        self._height: float = dict_frame["height"]
        self._rotate: float = dict_frame.get("rotate", None)

    @property
    def width(self) -> float:
        return self.to_mm(self._width)

    @property
    def height(self) -> float:
        return self.to_mm(self._height)

    @property
    def rotate(self) -> float:
        return self._rotate


class Value(Content):
    def __init__(self, dict_value: dict):
        super().__init__(dict_value)
        self.key: str = dict_value["key"]
        self.style: TextStyle = getattr(pdf_generation.text_style, dict_value["style"])()

    def to_text(self, content: Union[InvoiceContent, ServiceContent]) -> Text:
        return Text(
            {
                "text": reduce(getattr, self.key.split("."), content),
                "left": self._left,
                "top": self._top,
                "style": type(self.style).__name__,
            }
        )


class SwissQRCode:
    def __init__(self, dict_swiss_qr_code: dict):
        self.qr_code: Graphic = Graphic(dict_swiss_qr_code["qr_code"])
        self.swiss_cross: Graphic = Graphic(dict_swiss_qr_code["swiss_cross"])
