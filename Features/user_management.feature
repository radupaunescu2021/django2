# Created by hamburg at 20.10.2023
Feature: # Enter feature name here
  # Enter feature description here

   Scenario: Creating a new user
    When I send a POST request to "/api/users/" with user data
    Then I should receive a 201 Created response

  Scenario: User login and authentication
    Given I have created a user
    When I send a POST request to "/api/token/" with my credentials
    Then I should receive a 200 OK response with a token