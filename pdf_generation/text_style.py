from pathlib import Path

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


class TTFontToRegister:
    def __init__(self, path: Path, family: str):
        self.path = path
        self.family = family

    def register(self):
        pdfmetrics.registerFont(TTFont(self.family, self.path.resolve().as_posix()))


class TextStyle:
    def __init__(self, family: str = "Arial", size: float = 9, align: str = ""):
        self.family = family
        self.size = size
        self.align = align


class MainTitleTextStyle(TextStyle):
    def __init__(self, align: str = ""):
        super().__init__("Arial B", 16, align=align)


class DescriptorTextStyle(TextStyle):
    def __init__(self, align: str = ""):
        super().__init__("Arial B", 7, align=align)


class ContentTextStyle(TextStyle):
    def __init__(self, align: str = ""):
        super().__init__(align=align)


class ESRCodeTextStyle(TextStyle):
    def __init__(self, align: str = ""):
        super().__init__("OCRB", 10, align=align)
