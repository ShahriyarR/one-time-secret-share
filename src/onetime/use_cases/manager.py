import readonce
from dependency_injector.wiring import Provide

from onetime.services.manager import SecretManager, generate_and_encrypt_uuid
from onetime.use_cases.exceptions import (
    SecretDataWasAlreadyConsumedException,
    UUIDNotFoundException,
)


class SecretAndUrlManager:
    def __init__(self, secret_service: SecretManager = Provide["secret_manager"]):
        self.secret_service = secret_service
        self.uuid_storage = {}

    def generate_secret_and_url(self, secret: str) -> str:
        self.secret_service.generate_secret(secret)
        uuid = generate_and_encrypt_uuid()
        self.uuid_storage[uuid] = self.secret_service
        return uuid

    def get_secret(self, uuid: str) -> str:
        try:
            return self.uuid_storage[uuid].get_secret()
        except KeyError as e:
            raise UUIDNotFoundException("Failed to fetch the provided UUID") from e
        except readonce.UnsupportedOperationException as e:
            raise SecretDataWasAlreadyConsumedException(
                "Secret can not be retrieved twice, it was already consumed"
            ) from e
