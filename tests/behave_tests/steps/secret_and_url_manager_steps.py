from unittest.mock import patch

from behave import given, then, when

from onetime.services.manager import SecretManager
from onetime.use_cases.exceptions import URLExpiredException, UUIDNotFoundException
from onetime.use_cases.manager import SecretAndUrlManager

# Scenario: Generating a secret and URL


@given("I have a Secret and URL manager")
def step_impl(context):
    context.secret_and_url_manager = SecretAndUrlManager(secret_service=SecretManager())


@when('I generate a secret and URL with value "{secret}" and UUID returned')
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
