from typing import Union

from models import Author
from pdf_generation.contents.entity_content import EntityContent


class AuthorContent(EntityContent):
    def __init__(self, author: Author):
        super().__init__(author)
        self._author: Author = author

    @property
    def name(self) -> str:
        return self._author.name

    @property
    def email(self) -> str:
        return self._author.email

    @property
    def qr_iban(self) -> Union[str, None]:
        # TODO : Update when moving to QR-invoice
        _qr_iban: Union[str, None] = self._author.QRIBAN

        if _qr_iban:
            _qr_iban: str = _qr_iban.replace(" ", "")
            _qr_iban: str = " ".join(
                [_qr_iban[i : i + 4] for i in range(0, len(_qr_iban), 4)]
            )

        return _qr_iban
