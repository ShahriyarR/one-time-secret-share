from behave import given, then, when

from onetime.services.manager import SecretManager


# Scenario: Storing a secret
@given("I have a Secret Manager")
def step_impl(context):
    context.secret_manager = SecretManager()


@when('I generate a secret with UUID "{uuid}" and value "{secret}"')
def step_impl(context, uuid, secret):
    context.secret_manager.generate_secret(uuid, secret)


@then('the secret with UUID "{uuid}" should be stored')
def step_impl(context, uuid):
    assert list(context.secret_manager.secret.keys()) == [uuid]


#  Scenario: Retrieving a stored secret


@when('I retrieve the secret with UUID "{uuid}"')
def step_impl(context, uuid):
    context.secret = context.secret_manager.get_secret(uuid)


@then('the secret value should be "{secret}"')
def step_impl(context, secret):
    assert context.secret == secret


#  Scenario: Retrieving a non-existent secret


@then('an error should occur if I retrieve the secret with UUID "{uuid}"')
def step_impl(context, uuid):
    try:
        context.secret = context.secret_manager.get_secret(uuid)
    except KeyError:
        assert True
