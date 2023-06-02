import pytest
import readonce

from onetime.domain.model import Secret


def test_if_secret_object_can_be_created():
    secret_ = Secret(secret="awesome-password")
    assert secret_.get_secret() == "awesome-password"


def test_secret_cannot_read_twice():
    secret_ = Secret(secret="awesome-password")
    assert secret_.get_secret() == "awesome-password"

    with pytest.raises(readonce.UnsupportedOperationException):
        secret_.get_secret()
