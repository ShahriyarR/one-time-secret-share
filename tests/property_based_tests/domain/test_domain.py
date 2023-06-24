import pytest
from hypothesis import given
from hypothesis import strategies as st
from readonce import UnsupportedOperationException

from onetime.domain.model import Secret


@given(st.text())
def test_secret_retrieval(secret):
    # Create a Secret object
    secret_obj = Secret(secret)

    # Access the secret multiple times
    with pytest.raises(UnsupportedOperationException):
        for _ in range(5):
            secret_obj.get_secret()


@given(st.text(), st.text())
def test_secret_update(secret1, secret2):
    # Create a Secret object with the first secret
    secret_obj = Secret(secret1)

    # Add a new secret
    secret_obj.add_secret(secret2)

    # Verify that only last secret is stored
    assert secret_obj.get_secret() == secret2


@given(st.text(min_size=1))
def test_secret_length(secret):
    # Create a Secret object
    secret_obj = Secret(secret)

    # Verify that the secret length is preserved
    assert len(secret_obj.get_secret()) == len(secret)


@given(st.text(min_size=1))
def test_secret_substring(secret):
    # Create a Secret object
    secret_obj = Secret(secret)

    # Verify that the secret is a substring of the retrieved value
    retrieved_secret = secret_obj.get_secret()
    assert secret in retrieved_secret


@given(st.text(min_size=1))
def test_secret_empty_addition(secret):
    # Create a Secret object with the original secret
    secret_obj = Secret(secret)

    # Add an empty secret
    secret_obj.add_secret("")

    # Verify that the original secret is retrievable
    # So basically it is possible to create empty Secret.
    assert secret_obj.get_secret() == ""


@given(st.text(min_size=1))
def test_secret_whitespace_addition(secret):
    # Create a Secret object with the original secret
    secret_obj = Secret(secret)

    # Add a whitespace-only secret
    secret_obj.add_secret("   ")

    # Verify that the original secret is retrievable
    assert secret_obj.get_secret() == "   "


@given(st.text(min_size=1), st.text(min_size=1))
def test_secret_strip_addition(secret1, secret2):
    # Create a Secret object with the first secret
    secret_obj = Secret(secret1)

    # Add a secret with leading/trailing whitespace
    secret_obj.add_secret(f"  {secret2}  ")

    # Verify that the only last secret is available
    secret_ = secret_obj.get_secret()
    assert secret_ != secret1
    assert secret_ == f"  {secret2}  "
