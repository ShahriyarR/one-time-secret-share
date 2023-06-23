Feature: Secret and URL Manager
  As a user
  I would like to generate unique and random URLs and store the secret with this URLs.
  The URL itself is a symmetric encrypted string and stored in the dictionary as a key of the secret.

  Scenario: Generating a secret and URL
    Given I have a Secret and URL manager
    When I generate a secret and URL with value "MySecret"
    Then a UUID for the secret and URL should be returned

  Scenario: Retrieving a valid secret
    Given I have a Secret and URL manager
    And a secret and URL with UUID "123" is generated
    When I retrieve the secret with UUID "123"
    Then the secret value should be "MySecret"

  Scenario: Retrieving an expired URL
    Given I have a Secret Manager
    And an expired secret and URL with UUID "123" is generated
    When I retrieve the secret with UUID "123"
    Then an error should occur

  Scenario: Retrieving a non-existent secret
    Given I have a Secret Manager
    When I retrieve a secret with UUID "123"
    Then an error should occur

  Scenario: Retrieving a secret that was already consumed
    Given I have a Secret Manager
    And a secret and URL with UUID "123" is generated
    When I retrieve the secret with UUID "123" for the first time
    And I retrieve the secret with UUID "123" for the second time
    Then an error should occur

  Scenario: Generating multiple secrets and URLs
    Given I have a Secret Manager
    When I generate 5 secrets and URLs with value "MySecret"
    Then 5 UUIDs for the secrets and URLs should be returned

  Scenario: Retrieving multiple valid secrets
    Given I have a Secret Manager
    And 3 secrets and URLs are generated
    When I retrieve the secret with UUID "123"
    And I retrieve the secret with UUID "456"
    And I retrieve the secret with UUID "789"
    Then the secret values should be "Secret123", "Secret456", and "Secret789" respectively

  Scenario: Retrieving valid and non-existent secrets
    Given I have a Secret Manager
    And 2 secrets and URLs are generated
    When I retrieve the secret with UUID "123"
    And I retrieve a non-existent secret with UUID "999"
    Then the secret value should be "Secret123"
    And an error should occur

  Scenario: Generating secrets and URLs with different values
    Given I have a Secret Manager
    When I generate a secret and URL with value "MySecret1"
    And I generate a secret and URL with value "MySecret2"
    Then the secret values should be "MySecret1" and "MySecret2" respectively

  Scenario: Generating and retrieving secrets and URLs in random order
    Given I have a Secret Manager
    When I generate a secret and URL with value "MySecret"
    And I retrieve the secret with UUID "123"
    And I generate a secret and URL with value "AnotherSecret"
    And I retrieve the secret with UUID "456"
    Then the secret values should be "MySecret" and "AnotherSecret" respectively

