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

    def delete_cache(self, key: str):
        try:
            self._redis_client.delete(key)
            return True
        except Exception as e:
            print("[EX] AuthCacheRepository.delete_cache : ", str(e.args))
            return False

    def set_expire(self, key: str, expired_at: int):
        try:
            self._redis_client.expire(
                name=key,
                time=expired_at
            )
            return True
        except Exception as e:
            print("[EX] AuthCacheRepository.set_expire : ", str(e.args))
            return False