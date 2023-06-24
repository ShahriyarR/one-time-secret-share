Feature: Secret and URL Manager
  As a user
  I would like to generate unique and random URLs and store the secret with this URLs.
  The URL itself is a symmetric encrypted string and stored in the dictionary as a key of the secret.

  Scenario: Generating a secret and URL
    Given I have a Secret and URL manager
    When I generate a secret and URL with value "MySecret" and return UUID
    Then a UUID for the secret and URL should be stored

  Scenario: Retrieving a valid secret
    Given I have a Secret and URL manager
    When I generate a secret and URL with value "MySecret" and return UUID
    When I retrieve the secret with returned UUID
    Then the secret value should be "MySecret"
#
  Scenario: Retrieving an expired URL
    Given I have a Secret and URL manager
    When I generate a secret and URL with value "MySecret" and return UUID
    Then an error should occur if the URL was expired and I try to retrieve the secret
#
  Scenario: Retrieving a non-existent secret
    Given I have a Secret and URL manager
    Then  an error should occur if I retrieve a secret with non-existing UUID "123"

  Scenario: Retrieving a secret that was already consumed
    Given I have a Secret and URL manager
    When I generate a secret and URL with value "MySecret" and return UUID
    When I retrieve the secret with returned UUID
    Then and error should occur if I retrieve the secret with returned UUID for the second time

  Scenario: Generating multiple secrets and URLs
    Given I have a Secret and URL manager
    When I generate 5 secrets and URLs with value "MySecret"
    Then 5 UUIDs for the secrets and URLs should be returned

