# Created by hamburg at 20.10.2023
Feature: # Enter feature name here
  # Enter feature description here

#User,token creation


 ###Event creation
 Scenario: Creating a new event
    Given I am an authenticated user
    When I send a POST request to "/api/events/" with event data
    Then I should receive a 201 Created response

  Scenario: Listing all events
    Given I am an authenticated user
    When I send a GET request to "/api/events/"
    Then I should receive a 200 OK response with a list of events


    #Registering,unregistering
  Scenario: Registering for an event
    Given I am an authenticated user
    When I send a POST request to "/api/events/" with event data
    Then I should receive a 201 Created response
    #When I send a POST request to register to "/api/events/2/register/"
    When I send a POST request to register to event created previously
    Then I should receive a 201 Created response

  Scenario: Unregistering from an event
    Given I am an authenticated user
    When I send a POST request to "/api/events/" with event data
    Then I should receive a 201 Created response
    When I send a POST request to register to event created previously
    Then I should receive a 201 Created response
    When I send a DELETE request to unregister to the event created previously
    Then I should receive a 204 No Content response


  Scenario: Registering for an event with full capacity of 1
    Given I am an authenticated user with username "alice" and password "password1"
    When I send a POST request to "/api/events/" to create event with name "Popular Event" description "Music" start date "2023-12-25T10:00:00Z" end date "2023-12-26T10:00:00Z" capacity "1"
    When I send a POST request to register to event created previously
    Then I should receive a 201 Created response
    Given I am an authenticated user with username "bob" and password "password2"
    When I send a POST request to register to event created previously
    Then I should receive a 400 Bad Request response
    And The response should contain "The event has reached its maximum capacity."


  ####Listing events created by the user

  Scenario: Listing events created by the user
    Given I am an authenticated user
    When I send a POST request to "/api/events/" with event data
    When I send a GET request to "/api/events/user/"
    Then I should receive a 200 OK response with a list of events I have created



 Scenario: Users create and list their own events
    # Alice creates an event
    Given I am an authenticated user with username "alice" and password "password1"
    When I send a POST request to "/api/events/" to create event with name "Alice's Event" description "Alice's cool event" start date "2023-11-25T10:00:00Z" end date "2023-11-25T18:00:00Z" capacity "5"
    Then I should receive a 201 Created response

    # Bob creates an event
    Given I am an authenticated user with username "bob" and password "password2"
    When I send a POST request to "/api/events/" to create event with name "Bob's Event" description "Bob's cool event" start date "2023-12-25T10:00:00Z" end date "2023-12-25T18:00:00Z" capacity "5"
    Then I should receive a 201 Created response

    # Alice lists her events
    Given I am an authenticated user with username "alice" and password "password1"
    When I send a GET request to "/api/events/user/"
    Then I should receive a 200 OK response
    And The response should contain "Alice's Event" but not "Bob's Event"

    # Bob lists his events
    Given I am an authenticated user with username "bob" and password "password2"
    When I send a GET request to "/api/events/user/"
    Then I should receive a 200 OK response
    And The response should contain "Bob's Event" but not "Alice's Event"


  Scenario: Users create events and list all events
    # Alice creates an event
    Given I am an authenticated user with username "alice" and password "password1"
    When I send a POST request to "/api/events/" to create event with name "Alice's Event" description "Alice's cool event" start date "2023-11-25T10:00:00Z" end date "2023-11-25T18:00:00Z" capacity "5"
    Then I should receive a 201 Created response

    # Bob creates an event
    Given I am an authenticated user with username "bob" and password "password2"
    When I send a POST request to "/api/events/" to create event with name "Bob's Event" description "Bob's cool event" start date "2023-12-25T10:00:00Z" end date "2023-12-25T18:00:00Z" capacity "5"
    Then I should receive a 201 Created response

    # Alice lists all events
    Given I am an authenticated user with username "alice" and password "password1"
    When I send a GET request to "/api/events/"
    Then I should receive a 200 OK response
    And The response should contain both "Alice's Event" and "Bob's Event"




  #Refresh token
  Scenario: Refreshing access token
    Given I am an authenticated user
    And I am a user with a valid refresh token
    When I send a POST request to "/api/token/refresh/" with my refresh token
    Then I should receive a 200 OK response with a new access token


