Feature: Secret storage
  As a user
  I want to store and retrieve secrets using a Secret object.
  The Secret is a ReadOnce object.
  So that the secret is only accessible once.

  Scenario: Storing and retrieving a secret
    Given I have a secret "MySecret"
    When I store the secret using a Secret domain model
    And I retrieve the secret using the same Secret object
    Then I should get the secret value

  Scenario: Trying to retrieve a secret twice
    Given I have a secret "AnotherSecret"
    When I store the secret using a Secret domain model
    And I retrieve the secret using the same Secret object for the first time
    Then I should not get the secret value it should raise UnsupportedOperationException exception

  Scenario: Storing multiple secrets and retrieving them
    Given I have multiple secrets "Secret1", "Secret2", and "Secret3"
    When I store each secret using a Secret domain model
    And I retrieve each secret using the same Secret object
    Then I should get the corresponding secret values for each retrieval

  Scenario: Storing an empty secret
    Given I have an empty secret
    When I store the empty secret using a Secret domain model
    And I retrieve the secret using the same Secret object


  Scenario: Updating a stored secret
    Given I have a secret "MySecret"
    When I store the secret using a Secret domain model
    And I update the secret value to "NewSecret"
    And I retrieve the secret using the same Secret object
    Then I should get the updated secret value

  Scenario: Storing and retrieving a large secret
    Given I have a large secret
    When I store the secret using a Secret domain model
    And I retrieve the secret using the same Secret object
    Then I should get the complete secret value
