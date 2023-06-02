import pytest
import readonce

from onetime.services.manager import SecretManager


def test_if_secret_and_url_stored(get_secret_and_url_manager):
    uuid = get_secret_and_url_manager.generate_secret_and_url("awesome-password")
    assert get_secret_and_url_manager.uuid_storage
    secret_manager = get_secret_and_url_manager.uuid_storage[uuid]
    assert isinstance(secret_manager, SecretManager)
    # indeed the secret was reserved
    assert secret_manager.secret


def test_get_secret(get_secret_and_url_manager):
    uuid = get_secret_and_url_manager.generate_secret_and_url("awesome-password")
    secret_manager = get_secret_and_url_manager.uuid_storage[uuid]
    assert isinstance(secret_manager, SecretManager)
    # indeed the secret was reserved
    assert secret_manager.secret

    # retrieve secret
    assert get_secret_and_url_manager.get_secret(uuid) == "awesome-password"
    # try to get secret twice
    with pytest.raises(readonce.UnsupportedOperationException):
        get_secret_and_url_manager.get_secret(uuid)
