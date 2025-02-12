from enum import Enum
from typing import List, Union

class CommonEnum(Enum):
    """ Common enum class"""

    @classmethod
    def name_list(cls) -> List:
        """ return name list """
        return [data.name for data in cls]

    @classmethod
    def value_list(cls, key: Union[str, None] = None) -> List:
        """ return value list """
        if key is not None:
            return [getattr(data, key) for data in cls]
        return [data.value for data in cls]

    @classmethod
    def dict(cls) -> dict:
        """ return dict """
        return {data.name: data.value for data in cls}

    def __eq__(self, other) -> bool:
        """ check is equal with other value """
        if isinstance(other, CommonEnum):
            return self is other
        if self.value == other:
            return True
        return False
