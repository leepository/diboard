from typing import Optional

from app.domains.auth.repositories.repository import AuthRepository

class AuthHandler:
    def __init__(self, auth_repository: AuthRepository):
        self._repository = auth_repository

    def set_token(self, key: str, value: str, exp: int = 0) -> bool:
        try:
            self._repository.set_cache(key=key, value=value, exp=exp)
            return True
        except Exception as e:
            print("[EX] AuthHandler.set_token : ", str(e.args))
            return False

    def get_token(self, key: str) -> Optional[str]:
        try:
            cache_value = self._repository.get_cache(key=key)
            return cache_value
        except Exception as e:
            print("[EX] AuthHandler.get_token : ", str(e.args))
            return None
        