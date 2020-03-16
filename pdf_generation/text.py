from typing import Dict
from collections import namedtuple

import pdf_generation
from pdf_generation.text_style import TextStyle

class Text:
    def __init__(self, text: str, left: float, top: float, text_style: str):
        self.text: str = text
        self.left: float = left
        self.top: float = top
        self.text_style: TextStyle = getattr(pdf_generation.text_style, text_style)()

    @staticmethod
    def from_dict(dict_text: Dict) -> tuple:
        dict_text["text_style"] = getattr(pdf_generation.text_style, dict_text["text_style"])()
        return namedtuple("Text", dict_text.keys())(*dict_text.values())
