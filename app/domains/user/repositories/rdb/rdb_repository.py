from sqlalchemy import desc
from sqlalchemy.orm import Session
from typing import List, Type

from app.domains.user.models import User
from app.domains.user.repositories.repository import UserRepository
from app.utils.rdb_utils import DynamicFilter

class UserRdbRepository(UserRepository):
    def __init__(self, session: Session ):
        self.session = session

    def get_list(self, page: int, size: int)-> List[Type[User]]:
        offset = (page - 1) * size
        return self.session.query(User).order_by(desc(User.id)).offset(offset).limit(size).all()

    def get_detail(self, user_id: int = None, username: str = None) -> User:
        """
        Get user detail - user_id or username is required
        :param user_id: Optional
        :param username: Optional
        :return: User
        """
        filters = []
        if user_id is not None:
            filters.append({
                "field": "id",
                "op": "eq",
                "value": user_id
            })
        else:
            filters.append({
                "field": "username",
                "op": "eq",
                "value": username
            })
        user_filter = DynamicFilter(User)
        query = self.session.query(User)
        filtered_query = user_filter.apply_filters(query, filters)
        return filtered_query.first()

    def create(self, user: User) -> User:
        self.session.add(user)
        self.session.flush()
        return user

    def update(self, user: User) -> bool:
        self.session.merge(user)
        return True

    def delete(self, user: User) -> bool:
        self.session.delete(user)
        return True
