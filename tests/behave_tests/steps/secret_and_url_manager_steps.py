from unittest.mock import patch

from behave import given, then, when

from onetime.services.manager import SecretManager
from onetime.use_cases.exceptions import (
    SecretDataWasAlreadyConsumedException,
    URLExpiredException,
    UUIDNotFoundException,
)
from onetime.use_cases.manager import SecretAndUrlManager

# Scenario: Generating a secret and URL


@given("I have a Secret and URL manager")
def step_impl(context):
    context.secret_and_url_manager = SecretAndUrlManager(secret_service=SecretManager())


@when('I generate a secret and URL with value "{secret}" and return UUID')
def step_impl(context, secret):
    context.uuid = context.secret_and_url_manager.generate_secret_and_url(secret)


@then("a UUID for the secret and URL should be stored")
def step_impl(context):
    assert context.uuid in context.secret_and_url_manager.uuid_storage


#  Scenario: Retrieving a valid secret


@when("I retrieve the secret with returned UUID")
def step_impl(context):
    context.secret = context.secret_and_url_manager.get_secret(context.uuid)


# Scenario: Retrieving an expired URL


@then("an error should occur if the URL was expired and I try to retrieve the secret")
def step_impl(context):
    with patch("onetime.use_cases.manager.is_expired", return_value=True):
        try:
            context.secret = context.secret_and_url_manager.get_secret(context.uuid)
        except URLExpiredException:
            assert True


# Scenario: Retrieving a non-existent secret


@then('an error should occur if I retrieve a secret with non-existing UUID "{uuid}"')
def step_impl(context, uuid):
    try:
        context.secret = context.secret_and_url_manager.get_secret(uuid)
    except UUIDNotFoundException:
        assert True


# Scenario: Retrieving a secret that was already consumed


@then(
    "and error should occur if I retrieve the secret with returned UUID for the second time"
)
def step_impl(context):
    try:
        context.secret_2 = context.secret_and_url_manager.get_secret(context.uuid)
    except SecretDataWasAlreadyConsumedException:
        assert True


# Scenario: Generating multiple secrets and URLs


@when('I generate 5 secrets and URLs with value "{secret}"')
def step_impl(context, secret):
    context.uuids = [
        context.secret_and_url_manager.generate_secret_and_url(secret) for _ in range(5)
    ]
    assert len(context.uuids) == 5


@then("5 UUIDs for the secrets and URLs should be returned")
def step_impl(context):
    context.secrets = [
        context.secret_and_url_manager.get_secret(uuid) for uuid in context.uuids
    ]
    assert len(context.secrets) == 5
    assert all(secret == "MySecret" for secret in context.secrets)
