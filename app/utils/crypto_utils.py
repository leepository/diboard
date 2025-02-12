import base64
import hashlib

from app.common.config import get_config
from app.utils.common_utils import (
    get_api_env,
    get_ttl_hash
)

class CryptoHandler:

    def __init__(self):
        api_env = get_api_env()
        ttl_hash = get_ttl_hash()
        conf = get_config(ttl_hash=ttl_hash, api_env=api_env)
        self.salt = conf.KMS_SALT

    def encrypt_hash(self, plain_text: str) -> str:
        return base64.b64encode(hashlib.sha256((self.salt + plain_text).encode('utf-8')).digest()).decode('utf-8')

crypto_handler = CryptoHandler()
