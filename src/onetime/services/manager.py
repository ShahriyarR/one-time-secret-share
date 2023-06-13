from uuid import uuid4

from cryptography.fernet import Fernet

from onetime.domain.model import Secret


class SecretManager:
    def __init__(self):
        self.secret = {}

    def generate_secret(self, uuid: str, secret: str) -> None:
        self.secret[uuid] = Secret(secret)

    def get_secret(self, uuid: str) -> str:
        return self.secret[uuid].get_secret()


def generate_and_encrypt_uuid() -> str:
    uuid_ = str(uuid4())
    key = Fernet.generate_key()
    fernet = Fernet(key)
    uuid = fernet.encrypt(bytes(uuid_, encoding="utf-8"))
    return uuid.decode()
