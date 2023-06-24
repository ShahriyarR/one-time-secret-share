from behave import given, then, when
from readonce import UnsupportedOperationException

from onetime.domain.model import Secret


# Scenario: Storing and retrieving a secret
@given('I have a secret "{secret}"')
def step_impl(context, secret):
    context.secret = secret


@when("I store the secret using a Secret domain model")
def step_impl(context):
    context.secret_object = Secret(context.secret)


@when("I retrieve the secret using the same Secret object")
def step_impl(context):
    context.secret_ = context.secret_object.get_secret()


@then("I should get the secret value")
def step_impl(context):
    assert context.secret_ == "MySecret"


#  Scenario: Trying to retrieve a secret twice


@when("I retrieve the secret using the same Secret object for the first time")
def step_impl(context):
    context.secret_ = context.secret_object.get_secret()


@then(
    "I should not get the secret value it should raise UnsupportedOperationException exception"
)
def step_impl(context):
    try:
        context.secret_object.get_secret()
    except UnsupportedOperationException:
        assert True


#  Scenario: Storing multiple secrets and retrieving them


@given('I have multiple secrets "{secret1}", "{secret2}", and "{secret3}"')
def step_impl(context, secret1, secret2, secret3):
    context.secret1 = secret1
    context.secret2 = secret2
    context.secret3 = secret3


@when("I store each secret using a Secret domain model")
def step_impl(context):
    context.secret_object_1 = Secret(context.secret1)
    context.secret_object_2 = Secret(context.secret2)
    context.secret_object_3 = Secret(context.secret3)


@when("I retrieve each secret using the same Secret object")
def step_impl(context):
    context.secret_1 = context.secret_object_1.get_secret()
    context.secret_2 = context.secret_object_2.get_secret()
    context.secret_3 = context.secret_object_3.get_secret()


@then("I should get the corresponding secret values for each retrieval")
def step_impl(context):
    assert context.secret_1 == "Secret1"
    assert context.secret_2 == "Secret2"
    assert context.secret_3 == "Secret3"


#  Scenario: Storing an empty secret


@given("I have an empty secret")
def step_impl(context):
    context.secret = ""


@when("I store the empty secret using a Secret domain model")
def step_impl(context):
    context.secret_object = Secret(context.secret)


#  Scenario: Updating a stored secret


@when('I update the secret value to "{new_secret}"')
def step_impl(context, new_secret):
    context.secret_object.add_secret(new_secret)


@then("I should get the updated secret value")
def step_impl(context):
    assert context.secret_ == "NewSecret"


#  Scenario: Storing and retrieving a large secret


@given("I have a large secret")
def step_impl(context):
    context.secret = "Hello" * 2000


@then("I should get the complete secret value")
def step_impl(context):
    assert context.secret_ == context.secret
