from datetime import (
    datetime,
    timedelta
)

from app.common.config import get_config
from app.domains.auth.errors import AuthErrors
from app.domains.auth.schemas import AuthRequest
from app.domains.auth.handlers import AuthHandler
from app.domains.user.handlers import UserHandler
from app.utils.crypto_utils import crypto_handler
from app.utils.common_utils import (
    get_api_env,
    get_ttl_hash
)

class AuthService:
    def __init__(self, auth_handler: AuthHandler, user_handler: UserHandler):
        ttl_hash = get_ttl_hash()
        api_env = get_api_env()
        self.config = get_config(ttl_hash=ttl_hash, api_env=api_env)
        self.auth_handler = auth_handler
        self.user_handler = user_handler

    def signin(self, data: AuthRequest):
        # Get user data by username
        user = self.user_handler.get_detail(username=data.signin_id)
        if user is None:
            return AuthErrors.InvalidUsername

        # Compare password_hash to user data password hashed
        password_hash = crypto_handler.encrypt_hash(plain_text=data.signin_pass)
        if password_hash != user.password:
            return AuthErrors.InvalidPassword

        # Create refresh token and set cache
        refresh_token_expires_at = datetime.now() + timedelta(seconds=self.config.JWT_REFRESH_TOKEN_EXPIRES_SECONDS)
        refresh_token = self.auth_handler.create_refresh_token(expires_at=refresh_token_expires_at, subject=str(user.id))
        self.auth_handler.set_token(
            key=refresh_token,
            value=user.id,
            exp=self.config.JWT_REFRESH_TOKEN_EXPIRES_SECONDS
        )

        # Create access token and set cache
        access_token_expires_at = datetime.now() + timedelta(seconds=self.config.JWT_ACCESS_TOKEN_EXPIRES_SECONDS)
        access_token = self.auth_handler.create_access_token(expires_at=access_token_expires_at, subject=str(user.id))
        self.auth_handler.set_token(
            key=access_token,
            value=f"{user.id}",
            exp=self.config.JWT_ACCESS_TOKEN_EXPIRES_SECONDS
        )
        self.auth_handler.set_token(
            key=f"RT-{user.id}",
            value=f"{user.id}",
            exp=self.config.JWT_ACCESS_TOKEN_EXPIRES_SECONDS
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }


    def signout(self, access_token: str, refresh_token: str):
        access_token_value = self.auth_handler.get_token(key=access_token)
        refresh_token_key = self.auth_handler.get_token(key=f"RT-{access_token_value}")
        result_flag = self.auth_handler.delete_token(key=refresh_token_key)
        if result_flag is True:
            result_flag = self.auth_handler.delete_token(key=access_token)

        return result_flag
