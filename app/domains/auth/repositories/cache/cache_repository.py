from redis import Redis

from app.domains.auth.repositories.repository import AuthRepository

class AuthCacheRepository(AuthRepository):
    def __init__(self, redis_client: Redis):
        self._redis_client = redis_client

    def set_cache(self, key: str, value: str, exp: int = 0):
        if exp > 0:
            self._redis_client.set(
                name=key,
                value=value,
                ex=exp
            )
        else:
            self._redis_client.set(
                name=key,
                value=value
            )

    def get_cache(self, key: str):
        return self._redis_client.get(name=key)
