from models import Author
from .entity_content import EntityContent


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
    def iban(self) -> str:
        iban: str = self._author.IBAN
        iban: str = " ".join([iban[i : i + 4] for i in range(0, len(iban), 4)])

        return iban
