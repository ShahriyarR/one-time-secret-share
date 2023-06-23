Feature: Secret Manager
  As a user
  Secret Manager is for managing and storing the Secret objects.

  Scenario: Storing a secret
    Given I have a Secret Manager
    When I generate a secret with UUID "123" and value "MySecret"
    Then the secret with UUID "123" should be stored

  Scenario: Retrieving a stored secret
    Given I have a Secret Manager
    When I generate a secret with UUID "123" and value "MySecret"
    When I retrieve the secret with UUID "123"
    Then the secret value should be "MySecret"

  Scenario: Retrieving a non-existent secret
    Given I have a Secret Manager
    Then an error should occur if I retrieve the secret with UUID "123"

