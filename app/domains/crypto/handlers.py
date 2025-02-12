import base64
import boto3
import hashlib

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

class CryptoHandler:

    def __init__(self, conf: dict, client: boto3.client):
        self._client = client
        self._key_id = conf['KMS_ARN']
        self._salt = conf['KMS_SALT']
        self._key_spec = conf['KEY_SPEC']
        self._kms_key_id = conf['KMS_KEY_ID']
        self._kms_encryption_algorithm = conf['KMS_ENCRYPTION_ALGORITHM']

        # Data key 생성
        data_key = self._client.generate_data_key(
            KeyId=self._key_id,
            KeySpec=self._key_spec
        )
        self._plaintext_key = data_key.get("Plaintext")
        self._ciphertext_blob = data_key.get("CiphertextBlob")

    def _run_encrypt(self, cipher, iv, data):
        """ Encrypt data """
        return base64.b64encode(iv + cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))).decode('utf-8')

    def _run_decrypt(self, cipher, raw):
        """ Decrypt data """
        return unpad(cipher.decrypt(raw[AES.block_size:]), AES.block_size).decode('utf-8')

    def encrypt_hash(self, plain_text):
        return base64.b64encode(hashlib.sha256((self._salt + plain_text).encode('utf-8')).digest()).decode('utf-8')

    def check_hash(self, plain_text, hashed_value):
        hashed_text = self.encrypt_hash(plain_text)
        return True if hashed_text == hashed_value else False

    def encrypt_data(self, data):
        iv = get_random_bytes(AES.block_size)
        cipher = AES.new(self._plaintext_key, AES.MODE_CBC, iv)
        enc_data = self._run_encrypt(cipher, iv, data)
        cipher_text = base64.b64encode(self._ciphertext_blob).decode('utf-8')
        return enc_data, cipher_text

