from app.databases.transactions import TransactionManager
from app.domains.user.handlers import UserHandler
from app.domains.user.models import User
from app.utils.crypto_utils import crypto_handler

class UserService():

    def __init__(self, user_handler: UserHandler, transaction_manager: TransactionManager):
        self.user_handler = user_handler
        self.transaction_manager = transaction_manager

    def get_list(self, page: int, size: int):
        return self.user_handler.get_list(page=page, size=size)

    def get_detail(self, user_id: int = None, username: str = None):
        return self.user_handler.get_detail(user_id=user_id, username=username)

    def create_user(self, user: User):
        with self.transaction_manager.transaction():
            user.password = crypto_handler.encrypt_hash(plain_text=user.password)
            return self.user_handler.create(user=user)

    def delete_user(self, user_id) -> bool:
        with self.transaction_manager.transaction():
            return self.user_handler.delete(user_id)