from abc import ABC, abstractmethod

from app.domains.user.models import User

class UserRepository(ABC):

    @abstractmethod
    def get_list(self, page: int, size: int):
        pass

    @abstractmethod
    def get_detail(self, user_id: int):
        pass