from sqlalchemy.orm import Session

from app.domains.user.models import User
from app.domains.user.repositories.repository import UserRepository
from app.utils.rdb_utils import DynamicFilter

class UserRdbRepository(UserRepository):
    def __init__(self, session: Session ):
        self._session = session

    def get_list(self, page: int, size: int):
        offset = (page - 1) * size
        return self._session.query(User).offset(offset).limit(size).all()

    def get_detail(self, user_id: int = None, username: str = None):
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
        query = self._session.query(User)
        filtered_query = user_filter.apply_filters(query, filters)

        return filtered_query.first()

    def create(self, user: User):
        self._session.add(user)
        self._session.commit()
        self._session.refresh(user)
        return user

    def update(self, user: User):
        self._session.commit()
        self._session.refresh(user)
        return user

    def delete(self, user: User):
        self._session.delete(user)
        self._session.refresh(user)
        return user
