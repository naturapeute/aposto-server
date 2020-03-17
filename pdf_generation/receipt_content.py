from typing import Dict
from datetime import datetime, timezone


class ReceiptContent:
    def __init__(self, receipt_content_dict: Dict):
        self._receipt_content_dict: Dict = receipt_content_dict
        self._date: datetime = datetime.utcfromtimestamp(
            self._receipt_content_dict["timestamp"] / 1000
        ).replace(tzinfo=timezone.utc)

    @property
    def timestamp(self) -> str:
        return str(int(self._date.timestamp() * 1000))[:-3]

    @property
    def fullDateString(self) -> str:
        return self._date.strftime("%d.%m.%Y %H:%M:%S")

    @property
    def identification(self) -> str:
        return f"{self.timestamp} · {self.fullDateString}"
