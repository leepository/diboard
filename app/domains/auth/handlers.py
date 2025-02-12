from datetime import (
    datetime,
    timedelta
)

from jmespath.ast import identity
from jose import jwt
from typing import Optional, Union

from app.common.config import get_config
from app.domains.auth.repositories.repository import AuthRepository
from app.utils.common_utils import get_ttl_hash, get_api_env

class AuthHandler:
    def __init__(self, auth_repository: AuthRepository):
        api_env = get_api_env()
        ttl_hash = get_ttl_hash()
        self.config = get_config(ttl_hash=ttl_hash, api_env=api_env)
        self.auth_repository = auth_repository

    def set_token(self, key: str, value: str, exp: int = 0) -> bool:
        try:
            self.auth_repository.set_cache(key=key, value=value, exp=exp)
            return True
        except Exception as e:
            print("[EX] AuthHandler.set_token : ", str(e.args))
            return False

    def get_token(self, key: str) -> Optional[str]:
        try:
            cache_value = self.auth_repository.get_cache(key=key)
            return cache_value
        except Exception as e:
            print("[EX] AuthHandler.get_token : ", str(e.args))
            return None

    def delete_token(self, key: str):
        return self.auth_repository.delete_cache(key=key)

    def create_access_token(self, subject: str = None, expires_at: datetime = None):
        if subject is None:
            subject = ""
        if expires_at is None:
            expires_at = datetime.now() + timedelta(minutes=self.config.JWT_ACCESS_TOKEN_EXPIRES_MINUTES)

        claim = {"exp": expires_at, "sub": subject}
        token = jwt.encode(claim, self.config.JWT_ACCESS_SECRET_KEY, self.config.JWT_ALGORITHM)
        return token

    def create_refresh_token(self, subject: str = None, expires_at: datetime = None):
        if subject is None:
            subject = ""
        if expires_at is None:
            expires_at = datetime.now() + timedelta(minutes=self.config.JWT_REFRESH_TOKEN_EXPIRES_MINUTES)

        claim = {"exp": expires_at, "sub": subject}
        token = jwt.encode(claim, self.config.JWT_REFRESH_SECRET_KEY, self.config.JWT_ALGORITHM)
        return token

    def decode_access_token(self, token: str, options=None):
        payload = jwt.decode(
            token=token,
            key=self.config.JWT_ACCESS_SECRET_KEY,
            algorithms=self.config.JWT_ALGORITHM,
            options=options
        )
        identity = payload['sub']

        return identity

    def get_access_token_value(self, token: str):
        get_token_value = self.get_token(key=token)
        if get_token_value is None:
            return None
        self.auth_repository.set_expire(
            key=token,
            expired_at=self.config.JWT_ACCESS_TOKEN_EXPIRES_SECONDS
        )
        return get_token_value
