from uuid import uuid4

import pytest
import readonce

from onetime.domain.model import Secret
from onetime.services.manager import SecretManager


def test_if_secret_manager_object_created(get_secret_manager):
    assert get_secret_manager.secret == {}


def test_if_secret_is_generated(get_secret_manager):
    uuid_ = uuid4()
    get_secret_manager.generate_secret(uuid_, "awesome-secret")
    assert get_secret_manager.secret
    assert isinstance(get_secret_manager.secret[uuid_], Secret)


def test_if_secret_can_be_retrieved(get_secret_manager):
    uuid_ = uuid4()
    get_secret_manager.generate_secret(uuid_, "awesome-secret")
    assert get_secret_manager.secret
    assert get_secret_manager.get_secret(uuid_) == "awesome-secret"


def test_if_secret_can_not_be_retrieved_twice(get_secret_manager):
    uuid_ = uuid4()
    get_secret_manager.generate_secret(uuid_, "awesome-secret")
    assert get_secret_manager.secret
    assert get_secret_manager.get_secret(uuid_) == "awesome-secret"
    with pytest.raises(readonce.UnsupportedOperationException):
        get_secret_manager.get_secret(uuid_)


def test_if_two_secret_objects_are_not_equal(get_secret_manager):
    get_secret_manager.generate_secret(uuid4(), "awesome-secret")
    assert get_secret_manager.secret
    new_secret_manager = SecretManager()
    new_secret_manager.generate_secret(uuid4(), "awesome-secret")
    assert new_secret_manager.secret
    assert new_secret_manager is not get_secret_manager
    assert new_secret_manager != get_secret_manager
