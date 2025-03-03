from enum import Enum
from typing import List

class CustomErrors(Enum):
    def __init__(self, code: str, status_code: int, detail: str):
        self.code = code
        self.status_code = status_code
        self.detail = detail

    @classmethod
    def dict(cls) -> dict:
        return {
            data.code: {
                "code": data.code,
                "status_code": data.status_code,
                "detail": data.detail
            } for data in cls
        }

    @classmethod
    def list(cls) -> List:
        return [
            {
                "code": data.code,
                "status_code": data.name,
                "detail": data.detail
            } for data in cls
        ]

    @property
    def value(self) -> str:
        return self.code
