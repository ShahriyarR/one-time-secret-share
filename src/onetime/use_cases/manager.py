import datetime

import readonce
from dependency_injector.wiring import Provide

from onetime.configurator.settings import URL_EXPIRE_TTL
from onetime.services.manager import SecretManager, generate_and_encrypt_uuid
from onetime.use_cases.exceptions import (
    SecretDataWasAlreadyConsumedException,
    URLExpiredException,
    UUIDNotFoundException,
)
from onetime.use_cases.validators import is_expired


class SecretAndUrlManager:
    def __init__(self, secret_service: SecretManager = Provide["secret_manager"]):
        self.secret_service = secret_service
        self.uuid_storage = {}

    def generate_secret_and_url(self, secret: str) -> str:
        self.secret_service.generate_secret(secret)
        uuid = generate_and_encrypt_uuid()
        self.uuid_storage[uuid] = {
            "secret": self.secret_service,
            "created_at": datetime.datetime.now(),
        }
        return uuid

    def get_secret(self, uuid: str) -> str:
        try:
            # expect to raise URLExpiredException if the URL expired
            return self._get_secret(uuid)
        except KeyError as e:
            raise UUIDNotFoundException(
                "Could not find the secret with provided UUID"
            ) from e
        except readonce.UnsupportedOperationException as e:
            raise SecretDataWasAlreadyConsumedException(
                "Secret can not be retrieved twice, it was already consumed"
            ) from e

    def _get_secret(self, uuid: str) -> str:
        if not is_expired(
            self.uuid_storage[uuid]["created_at"], expire_after=URL_EXPIRE_TTL
        ):
            return self.uuid_storage[uuid]["secret"].get_secret()
        # If we got here then the link is expired; first remove the URL and raise exception
        del self.uuid_storage[uuid]
        raise URLExpiredException("URL with given UUID is expired")
