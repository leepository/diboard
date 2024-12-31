from enum import Enum

class OptionMeta(Enum):
    def __init__(self, code: str, name: str, sort: int, is_display: bool):
        self.code = code
        self.name = name
        self.sort = sort
        self.is_display = is_display

    @classmethod
    def dict(cls) -> dict:
        return {
            data.code : {
                "code": data.code,
                "name": data.name,
                "sort": data.sort,
                "is_display": data.is_display
            } for data in cls
        }

    @classmethod
    def list(cls) -> list:
        return [
            {
                "code": data.code,
                "name": data.name,
                "sort": data.sort,
                "is_display": data.is_display
            } for data in cls
        ]

    @classmethod
    def display_list(cls) -> list:
        return [
            {
                "code": data.code,
                "name": data.name,
                "sort": data.sort,
                "is_display": data.is_display
            } for data in cls if data.is_display is True
        ]

    @property
    def value(self):
        return self.code
