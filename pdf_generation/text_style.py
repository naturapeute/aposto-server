from pathlib import Path

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


class TTFontToRegister:
    def __init__(self, path: Path, family: str):
        self.path: Path = path
        self.family: str = family

    def register(self):
        pdfmetrics.registerFont(TTFont(self.family, self.path.resolve().as_posix()))


class TextStyle:
    def __init__(self, family: str = "Arial", size: float = 9, align: str = ""):
        self.family: str = family
        self.size: float = size
        self.align: str = align


class TitleTextStyle(TextStyle):
    def __init__(self):
        super().__init__("Arial B", 16)


class DescriptorTextStyle(TextStyle):
    def __init__(self):
        super().__init__("Arial", 7)


class DescriptorRightTextStyle(DescriptorTextStyle):
    def __init__(self):
        super().__init__()
        self.align = "R"


class DescriptorCenteredTextStyle(DescriptorTextStyle):
    def __init__(self):
        super().__init__()
        self.align = "C"


class BoldDescriptorTextStyle(DescriptorTextStyle):
    def __init__(self):
        super().__init__()
        self.family = "Arial B"


class BoldDescriptorRightTextStyle(BoldDescriptorTextStyle):
    def __init__(self):
        super().__init__()
        self.align = "R"


class BoldDescriptorCenteredTextStyle(BoldDescriptorTextStyle):
    def __init__(self):
        super().__init__()
        self.align = "C"


class ValueTextStyle(TextStyle):
    def __init__(self):
        super().__init__()


class ValueRightTextStyle(ValueTextStyle):
    def __init__(self):
        super().__init__()
        self.align = "R"


class ValueCenteredTextStyle(ValueTextStyle):
    def __init__(self):
        super().__init__()
        self.align = "C"


class BoldValueRightTextStyle(ValueTextStyle):
    def __init__(self):
        super().__init__()
        self.family = "Arial B"
        self.align = "R"


class SmallValueTextStyle(ValueTextStyle):
    def __init__(self):
        super().__init__()
        self.size = 7


class SmallValueCenteredTextStyle(SmallValueTextStyle):
    def __init__(self):
        super().__init__()
        self.align = "C"


class SmallValueRightTextStyle(SmallValueTextStyle):
    def __init__(self):
        super().__init__()
        self.align = "R"


class SmallBoldValueTextStyle(TextStyle):
    def __init__(self):
        super().__init__()
        self.family = "Arial B"
        self.size = 7


class ESRCodeTextStyle(TextStyle):
    def __init__(self):
        super().__init__("OCRB", 10)


class QRInvoiceMainTitleTextStyle(TextStyle):
    def __init__(self):
        super().__init__("Arial B", 11)


class QRInvoicePaymentSectionTextStyle(TextStyle):
    def __init__(self):
        super().__init__(size=10)


class QRInvoicePaymentSectionHeaderTextStyle(QRInvoiceMainTitleTextStyle):
    def __init__(self):
        super().__init__(size=8)


class QRInvoiceReceiptTextStyle(TextStyle):
    def __init__(self):
        super().__init__(size=8)


class QRInvoiceReceiptHeaderTextStyle(QRInvoiceMainTitleTextStyle):
    def __init__(self):
        super().__init__(size=6)
