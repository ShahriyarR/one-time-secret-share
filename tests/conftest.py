import pytest

from onetime.services.manager import SecretManager
from onetime.use_cases.manager import SecretAndUrlManager


@pytest.fixture(scope="module")
def get_secret_manager():
    return SecretManager()


@pytest.fixture(scope="module")
def get_secret_and_url_manager(get_secret_manager):
    return SecretAndUrlManager(secret_service=get_secret_manager)
