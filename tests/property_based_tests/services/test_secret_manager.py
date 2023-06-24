import pytest
from hypothesis import assume, given
from hypothesis import strategies as st
from readonce import UnsupportedOperationException

from onetime.services.manager import SecretManager


@given(st.uuids(), st.text())
def test_secret_retrieval(uuid, secret):
    # Create a SecretManager object
    manager = SecretManager()

    # Generate a secret
    manager.generate_secret(uuid, secret)

    # Verify that the generated secret can be retrieved
    assert manager.get_secret(uuid) == secret


@given(st.uuids())
def test_nonexistent_secret_retrieval(uuid):
    # Create a SecretManager object
    manager = SecretManager()

    # Verify that retrieving a non-existent secret raises a KeyError
    try:
        manager.get_secret(uuid)
    except KeyError:
        pass
    else:
        assert False, "Expected KeyError"


@given(st.uuids(), st.text())
def test_multiple_secret_retrieval(uuid, secret):
    # Create a SecretManager object
    manager = SecretManager()

    # Generate a secret
    manager.generate_secret(uuid, secret)

    # Retrieve the secret multiple times
    assert manager.get_secret(uuid) == secret
    with pytest.raises(UnsupportedOperationException):
        assert manager.get_secret(uuid) == secret


@given(st.uuids(), st.uuids(), st.text(), st.text())
def test_independent_secret_storage(uuid1, uuid2, secret1, secret2):
    assume(uuid1 != uuid2)  # Ensure different UUIDs

    # Create a SecretManager object
    manager = SecretManager()

    # Generate secrets for different UUIDs
    manager.generate_secret(uuid1, secret1)
    manager.generate_secret(uuid2, secret2)

    # Verify that the secrets are stored independently
    assert manager.get_secret(uuid1) == secret1
    assert manager.get_secret(uuid2) == secret2


@given(st.uuids(), st.text(), st.text())
def test_secret_overwrite(uuid, secret1, secret2):
    # Create a SecretManager object
    manager = SecretManager()

    # Generate two secrets with the same UUID
    manager.generate_secret(uuid, secret1)
    manager.generate_secret(uuid, secret2)

    # Verify that the second secret overwrites the first secret
    assert manager.get_secret(uuid) == secret2


@given(st.uuids())
def test_empty_manager_retrieval(uuid):
    # Create an empty SecretManager object
    manager = SecretManager()

    # Verify that retrieving a secret from an empty manager raises a KeyError
    try:
        manager.get_secret(uuid)
    except KeyError:
        pass
    else:
        assert False, "Expected KeyError"


@given(st.uuids(), st.text())
def test_shared_secret(uuid, secret):
    # Create two SecretManager objects
    manager1 = SecretManager()
    manager2 = SecretManager()

    # Generate a secret in one manager
    manager1.generate_secret(uuid, secret)

    # Verify that the secrets are not shared
    assert manager1.get_secret(uuid) == secret
    with pytest.raises(KeyError):
        assert manager2.get_secret(uuid)


@given(st.uuids(), st.uuids(), st.text(), st.text())
def test_no_affect_previous_secrets(uuid1, uuid2, secret1, secret2):
    assume(uuid1 != uuid2)  # Ensure different UUIDs

    # Create a SecretManager object
    manager = SecretManager()

    # Generate a secret
    manager.generate_secret(uuid1, secret1)

    # Generate another secret with a different UUID
    manager.generate_secret(uuid2, secret2)

    # Verify that the first secret is still retrievable
    assert manager.get_secret(uuid1) == secret1


@given(st.uuids(), st.text())
def test_empty_string_secret(uuid, secret):
    # Create a SecretManager object
    manager = SecretManager()

    # Generate a secret with an empty string
    manager.generate_secret(uuid, "")

    # Verify that the secret is retrievable
    assert manager.get_secret(uuid) == ""


@given(st.uuids(), st.text())
def test_whitespace_secret(uuid, secret):
    # Create a SecretManager object
    manager = SecretManager()

    # Generate a secret with a whitespace-only string
    manager.generate_secret(uuid, "   ")

    # Verify that the secret is retrievable
    assert manager.get_secret(uuid) == "   "
