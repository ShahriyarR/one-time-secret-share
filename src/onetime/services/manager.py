from uuid import uuid4

from cryptography.fernet import Fernet

from onetime.domain.model import Secret


class SecretManager:
    def __init__(self):
        self.secret = None

    def generate_secret(self, secret: str) -> None:
        self.secret = Secret(secret)

    def get_secret(self) -> str:
        return self.secret.get_secret()


def generate_and_encrypt_uuid() -> str:
    uuid_ = str(uuid4())
    key = Fernet.generate_key()
    fernet = Fernet(key)
    uuid = fernet.encrypt(bytes(uuid_, encoding="utf-8"))
    return str(uuid)
