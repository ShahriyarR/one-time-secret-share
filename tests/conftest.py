import pytest

from onetime.services.manager import SecretManager


@pytest.fixture(scope="module")
def get_secret_manager():
    return SecretManager()
