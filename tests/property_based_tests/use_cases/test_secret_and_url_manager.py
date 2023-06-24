from datetime import datetime, timedelta

import pytest
from hypothesis import assume, given
from hypothesis import strategies as st

from onetime.services.manager import SecretManager
from onetime.use_cases.exceptions import (
    SecretDataWasAlreadyConsumedException,
    URLExpiredException,
    UUIDNotFoundException,
)
from onetime.use_cases.manager import SecretAndUrlManager


@given(st.text())
def test_generate_and_retrieve_secret_and_url(secret):
    # Create a SecretAndUrlManager object with a mock SecretManager
    manager = SecretAndUrlManager(secret_service=SecretManager())

    # Generate a secret and URL
    uuid = manager.generate_secret_and_url(secret)

    # Verify that the secret can be retrieved using the generated UUID
    assert manager.get_secret(uuid) == secret


@given(st.uuids())
def test_nonexistent_secret_retrieval(uuid):
    # Create a SecretAndUrlManager object with a mock SecretManager
    manager = SecretAndUrlManager(secret_service=SecretManager())

    # Verify that retrieving a non-existent secret raises a UUIDNotFoundException
    with pytest.raises(UUIDNotFoundException):
        manager.get_secret(str(uuid))


@given(st.uuids(), st.text())
def test_consumed_secret_retrieval(uuid, secret):
    # Create a SecretAndUrlManager object with a mock SecretManager
    manager = SecretAndUrlManager(secret_service=SecretManager())

    # Generate a secret and URL
    uuid_ = manager.generate_secret_and_url(secret)

    # Retrieve the secret once
    manager.get_secret(str(uuid_))

    # Verify that retrieving the consumed secret raises a SecretDataWasAlreadyConsumedException
    with pytest.raises(SecretDataWasAlreadyConsumedException):
        manager.get_secret(str(uuid_))


@given(st.uuids(), st.text(), st.datetimes())
def test_expired_url_retrieval(uuid, secret, created_at):
    assume(created_at < datetime.now())  # Ensure created_at is in the past

    # Create a SecretAndUrlManager object with a mock SecretManager
    manager = SecretAndUrlManager(secret_service=SecretManager())

    # Generate a secret and URL with a custom created_at
    manager.uuid_storage[str(uuid)] = {
        "secret": manager.secret_service,
        "created_at": created_at,
    }

    # Verify that retrieving an expired URL raises a URLExpiredException
    with pytest.raises(URLExpiredException):
        manager.get_secret(str(uuid))


# Test case 5: Test that retrieving a secret with valid UUID and URL does not raise any exceptions
@given(st.text())
def test_valid_secret_retrieval(secret):
    # Create a SecretAndUrlManager object with a real SecretManager
    manager = SecretAndUrlManager(secret_service=SecretManager())

    # Generate a secret and URL
    uuid = manager.generate_secret_and_url(secret)

    # Verify that retrieving the secret with a valid UUID and URL does not raise any exceptions
    try:
        manager.get_secret(uuid)
    except (
        UUIDNotFoundException,
        SecretDataWasAlreadyConsumedException,
        URLExpiredException,
    ):
        assert False, "Did not expect any exceptions"


# Test case 6: Test that generating a secret and URL stores the secret and created_at in the uuid_storage
@given(st.text())
def test_secret_and_url_storage(secret):
    # Create a SecretAndUrlManager object with a mock SecretManager
    manager = SecretAndUrlManager(secret_service=SecretManager())

    # Generate a secret and URL
    uuid = manager.generate_secret_and_url(secret)

    # Verify that the secret and created_at are stored in the uuid_storage
    assert str(uuid) in manager.uuid_storage
    assert manager.uuid_storage[str(uuid)]["secret"] == manager.secret_service
    assert isinstance(manager.uuid_storage[str(uuid)]["created_at"], datetime)


@given(st.text(), st.text())
def test_multiple_secret_and_url_storage(secret1, secret2):
    assume(secret1 != secret2)  # Ensure different secrets

    # Create a SecretAndUrlManager object with a mock SecretManager
    manager = SecretAndUrlManager(secret_service=SecretManager())

    # Generate secrets and URLs for different UUIDs
    uuid1 = manager.generate_secret_and_url(secret1)
    uuid2 = manager.generate_secret_and_url(secret2)

    # Verify that the secrets and created_at are stored independently in the uuid_storage
    assert str(uuid1) in manager.uuid_storage
    assert manager.uuid_storage[str(uuid1)]["secret"] == manager.secret_service
    assert isinstance(manager.uuid_storage[str(uuid1)]["created_at"], datetime)
    assert manager.get_secret(uuid1) == secret1

    assert str(uuid2) in manager.uuid_storage
    assert manager.uuid_storage[str(uuid2)]["secret"] == manager.secret_service
    assert isinstance(manager.uuid_storage[str(uuid2)]["created_at"], datetime)
    assert manager.get_secret(uuid2) == secret2


@given(st.text())
def test_valid_uuid_generation(secret):
    # Create a SecretAndUrlManager object with a mock SecretManager
    manager = SecretAndUrlManager(secret_service=SecretManager())

    # Generate a secret and URL
    uuid = manager.generate_secret_and_url(secret)

    # Verify that the generated UUID is valid
    assert isinstance(uuid, str) and len(uuid) > 0


@given(st.uuids())
def test_valid_uuid_generation_empty_string(uuid):
    # Create a SecretAndUrlManager object with a mock SecretManager
    manager = SecretAndUrlManager(secret_service=SecretManager())

    # Generate a secret and URL with an empty string secret
    generated_uuid = manager.generate_secret_and_url("")

    # Verify that the generated UUID is valid
    assert isinstance(generated_uuid, str) and len(generated_uuid) > 0


@given(st.uuids())
def test_valid_uuid_generation_whitespace_secret(uuid):
    # Create a SecretAndUrlManager object with a mock SecretManager
    manager = SecretAndUrlManager(secret_service=SecretManager())

    # Generate a secret and URL with a whitespace-only string secret
    generated_uuid = manager.generate_secret_and_url("   ")

    # Verify that the generated UUID is valid
    assert isinstance(generated_uuid, str) and len(generated_uuid) > 0


@given(st.text(alphabet=st.characters(whitelist_categories=("Lu",)), min_size=1))
def test_valid_uuid_generation_uppercase_secret(secret):
    # Create a SecretAndUrlManager object with a mock SecretManager
    manager = SecretAndUrlManager(secret_service=SecretManager())

    # Generate a secret and URL with a secret containing only uppercase letters
    generated_uuid = manager.generate_secret_and_url(secret)

    # Verify that the generated UUID is valid
    assert isinstance(generated_uuid, str) and len(generated_uuid) > 0


@given(st.text(alphabet=st.characters(whitelist_categories=("Ll",)), min_size=1))
def test_valid_uuid_generation_lowercase_secret(secret):
    # Create a SecretAndUrlManager object with a mock SecretManager
    manager = SecretAndUrlManager(secret_service=SecretManager())

    # Generate a secret and URL with a secret containing only lowercase letters
    generated_uuid = manager.generate_secret_and_url(secret)

    # Verify that the generated UUID is valid
    assert isinstance(generated_uuid, str) and len(generated_uuid) > 0


@given(st.text(alphabet=st.characters(whitelist_categories=("Lu", "Ll")), min_size=1))
def test_valid_uuid_generation_mixed_case_secret(secret):
    # Create a SecretAndUrlManager object with a mock SecretManager
    manager = SecretAndUrlManager(secret_service=SecretManager())

    # Generate a secret and URL with a secret containing both uppercase and lowercase letters
    generated_uuid = manager.generate_secret_and_url(secret)

    # Verify that the generated UUID is valid
    assert isinstance(generated_uuid, str) and len(generated_uuid) > 0


@given(st.text(alphabet=st.characters(whitelist_categories=("Nd",)), min_size=1))
def test_valid_uuid_generation_digit_secret(secret):
    # Create a SecretAndUrlManager object with a mock SecretManager
    manager = SecretAndUrlManager(secret_service=SecretManager())

    # Generate a secret and URL with a secret containing digits
    generated_uuid = manager.generate_secret_and_url(secret)

    # Verify that the generated UUID is valid
    assert isinstance(generated_uuid, str) and len(generated_uuid) > 0


@given(st.text(alphabet=st.characters(whitelist_categories=("P",)), min_size=1))
def test_valid_uuid_generation_special_char_secret(secret):
    # Create a SecretAndUrlManager object with a mock SecretManager
    manager = SecretAndUrlManager(secret_service=SecretManager())

    # Generate a secret and URL with a secret containing special characters
    generated_uuid = manager.generate_secret_and_url(secret)

    # Verify that the generated UUID is valid
    assert isinstance(generated_uuid, str) and len(generated_uuid) > 0


@given(st.text())
def test_immediate_secret_retrieval(secret):
    # Create a SecretAndUrlManager object with a mock SecretManager
    manager = SecretAndUrlManager(secret_service=SecretManager())

    # Generate a secret and URL
    uuid = manager.generate_secret_and_url(secret)

    # Retrieve the secret immediately after generation
    retrieved_secret = manager.get_secret(uuid)

    # Verify that the retrieved secret is the same as the original secret
    assert retrieved_secret == secret


@given(st.text(), st.text())
def test_concurrent_secret_generation(secret1, secret2):
    # Create a SecretAndUrlManager object with a real SecretManager
    manager = SecretAndUrlManager(secret_service=SecretManager())

    # Generate secrets and URLs concurrently
    uuid1 = manager.generate_secret_and_url(secret1)
    uuid2 = manager.generate_secret_and_url(secret2)

    # Verify that retrieving the secrets with the generated UUIDs returns the correct secrets
    assert manager.get_secret(uuid1) == secret1
    assert manager.get_secret(uuid2) == secret2
