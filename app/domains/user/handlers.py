from typing import List, Type

from app.domains.user.models import User
from app.domains.user.repositories.repository import UserRepository

class UserHandler:
    def __init__(self, user_repository: UserRepository):
        self._repository = user_repository

    def get_list(self, page: int, size: int) -> List[Type[User]]:
        return self._repository.get_list(page=page, size=size)

    def get_detail(self, user_id: int = None, username: str = None) -> User:
        return self._repository.get_detail(user_id=user_id, username=username)

    def create(self, user: User) -> User:
        return self._repository.create(user=user)

    def update(self, user_id: int, requested_user: User) -> User:
        user = self._repository.get_detail(user_id=user_id)
        if user is None:
            return None

        for key, value in requested_user.model_dump().items():
            setattr(user, key, value)

        return self._repository.update(user=user)

    def delete(self, user_id: int) -> User:
        user = self._repository.get_detail(user_id=user_id)
        if user is None:
            return None
        return self._repository.delete(user=user)
