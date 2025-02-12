from abc import ABC, abstractmethod

class AuthRepository(ABC):

    @abstractmethod
    def set_cache(self, key: str, value: str, exp: int = 0):
        pass

    @abstractmethod
    def get_cache(self, key):
        pass

    @abstractmethod
    def delete_cache(self, key):
        pass

    @abstractmethod
    def set_expire(self, key, expired_at: int):
        pass