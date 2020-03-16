from typing import Dict
from collections import namedtuple

import pdf_generation
from pdf_generation.text_style import TextStyle

class Text:
    def __init__(self, dict_text: Dict):
        self.text: str = dict_text["text"]
        self._left: float = dict_text["left"]
        self._top: float = dict_text["top"]
        self.style: TextStyle = getattr(pdf_generation.text_style, dict_text["style"])()

    @staticmethod
    def from_dict(dict_text: Dict) -> tuple:
        dict_text["text_style"] = getattr(pdf_generation.text_style, dict_text["text_style"])()
        return namedtuple("Text", dict_text.keys())(*dict_text.values())
