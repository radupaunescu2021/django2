import logging

from behave import given, when, then
from django.contrib.auth.hashers import make_password
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model



@given('I have created a user')
def step_impl(context):
    User = get_user_model()
    context.user, created = User.objects.get_or_create(username='Behavenewuser', defaults={'password': 'Behavenewpass'})

@when('I send a POST request to "{url}" with user data')
def step_impl(context, url):
    context.client = APIClient()
    response = context.client.post(url, {
        'username': 'Behavenewuser',
        'password': 'Behavenewpass'
    }, format='json')
    context.response = response
    logging.info("Response content: %s", response.content)
    logging.info(context.response)

@when('I send a POST request to "{url}" with username "{username}" and password "{password}"')
def step_impl(context, url, username, password):
    context.client = APIClient()
    response = context.client.post(url, {
        'username': username,
        'password': password
    }, format='json')
    context.response = response
    logging.info("Response content: %s", response.content)
    logging.info(context.response)

@when('I send a POST request to "{url}" with my credentials')
def step_impl(context, url):
    context.client = APIClient()
    response = context.client.post(url, {
        'username': 'Behavenewuser',
        'password': 'Behavenewpass'
    }, format='json')
    context.response = response



@then('I should receive a 200 OK response with a token')
def step_impl(context):
    assert context.response.status_code == 200, context.response.content
    response_data = context.response.json()
    assert 'access' in response_data, context.response.content
    assert 'refresh' in response_data, context.response.content
    context.token = response_data['access']  # Save the access token to the context
    context.refresh_token = response_data['refresh']  # Save the refresh token to the context




@given('I am an authenticated user')
def step_impl(context):

   User = get_user_model()
   user, created = User.objects.get_or_create(
       username='Behavenewuser',
       defaults={'password': make_password('Behavenewpass')}
   )
   client = APIClient()
   response = client.post('/api/token/', {
       'username': 'Behavenewuser',
       'password': 'Behavenewpass'
   }, format='json')
   assert response.status_code == 200, response.content
   context.token = response.json()['access']
   context.refresh_token= response.json()['refresh']
   context.client = client
   context.client.credentials(HTTP_AUTHORIZATION=f'Bearer {context.token}')
   context.user=user


@given('I am an authenticated user with username "{username}" and password "{password}"')
def step_impl(context, username, password):
    User = get_user_model()
    user, created = User.objects.get_or_create(
        username=username,
        defaults={'password': make_password(password)})
    client = APIClient()
    response = client.post('/api/token/', {
        'username': username,
        'password': password
    }, format='json')
    assert response.status_code == 200, response.content
    context.token = response.json()['access']
    context.refresh_token = response.json()['refresh']
    context.client = client
    context.client.credentials(HTTP_AUTHORIZATION=f'Bearer {context.token}')



@when('I send a POST request to "{url}" with valid data')
def step_impl(context, url):
    response = context.client.post(url, {'name': 'Test Event', 'description': 'Test Description'}, format='json')
    context.response = response

#@then('I should receive a 201 Created response')
#def step_impl(context):
 #   print("Status responde code " +str(context.response.status_code))
  #  assert context.response.status_code == 201




@when('I send a POST request to "{url}" with event data')
def step_impl(context, url):
    response = context.client.post(url, {
        "name": "Test Event",
        "description": "Test Description",
        "start_date": "2024-11-25T10:00:00Z",
        "end_date": "2024-11-25T18:00:00Z"
        # ... other event data ...
    }, format='json')
    context.response = response
    response_data = response.json()  # Assuming response is an object with a json() method
    print("Event create"+str(response_data))
    logging.info("Event create"+str(response_data))
    #Save event id for later use
    event_id = response_data['id']
    context.event_id = event_id



@when('I send a POST request to "{url}" to create event with name "{name}" description "{description}" start date "{start_date}" end date "{end_date}" capacity "{capacity}')
def step_impl(context, url, name, description, start_date, end_date, capacity=None):
    print(f'Capacity argument: {capacity}')
    event_data = {
        "name": name,
        "description": description,
        "start_date": start_date,
        "end_date": end_date
    }
    # If the optional capacity is provided, add the capacity to the event data
    if capacity is not None:
        capacity = capacity.replace('"', '')
        event_data["capacity"] = int(capacity)  # Ensure capacity is an integer
    response = context.client.post(url, event_data, format='json')
    response_data = response.json()  # Assuming response is an object with a json() method
    event_id = response_data['id']

    #Save event id
    context.response = response
    context.event_id=event_id


@then('The response should contain "{included_event}" but not "{excluded_event}"')
def step_impl(context, included_event, excluded_event):
    response_data = context.response.json()

    # Assuming the response data is a list of event dictionaries
    # with each dictionary containing a 'name' key.
    event_names = [event['name'] for event in response_data]

    assert included_event in event_names, f"Expected to find '{included_event}' in response, but did not. Response: {response_data}"
    assert excluded_event not in event_names, f"Expected not to find '{excluded_event}' in response, but did. Response: {response_data}"

@then('The response should contain both "{event_name1}" and "{event_name2}"')
def step_impl(context, event_name1, event_name2):
    response_data = context.response.json()
    event_names = [event['name'] for event in response_data]
    assert event_name1 in event_names, f"Expected to find '{event_name1}' in response, but did not. Response: {response_data}"
    assert event_name2 in event_names, f"Expected to find '{event_name2}' in response, but did not. Response: {response_data}"


@when('I send a GET request to "{url}"')
def step_impl(context, url):
    response = context.client.get(url)
    context.response = response

@when('I send a POST request to register to "{url}"')
def step_impl(context, url):
    response = context.client.get(url)
    print("Events"+ str(response.json()))
    response = context.client.post(url)
    context.response = response
    print("registering to event"+ str(context.response))


@when('I send a POST request to register to event created previously')
def step_impl(context):
    url="/api/events/"+str(context.event_id)+"/register/"
    response = context.client.post(url)
    context.response = response

@when('I send a DELETE request to unregister to the event created previously')
def step_impl(context):
    url = "/api/events/" + str(context.event_id) + "/unregister/"
    response = context.client.delete(url)
    context.response = response

@then('I should receive a {status_code} {status_text} response')
def step_impl(context, status_code, status_text):
    assert context.response.status_code == int(status_code), context.response.content

# If you want to check the content of the response in the listing scenario:
@then('I should receive a 200 OK response with a list of events')
def step_impl(context):
    assert context.response.status_code == 200, context.response.content
    assert isinstance(context.response.json(), list), context.response.content
    logging.info("events: %s", context.response.json())





#####################refresh token

@given('I am a user with a valid refresh token')
def step_impl(context):
    # Assuming you have a way to obtain a refresh token for a user
    assert hasattr(context, 'refresh_token'), "Refresh token has not been set in the context"

@when('I send a POST request to "{url}" with my refresh token')
def step_impl(context, url):
    context.client = APIClient()
    response = context.client.post(url, {
        'refresh': context.refresh_token
    }, format='json')
    context.response = response

@then('I should receive a 200 OK response with a new access token')
def step_impl(context):
    assert context.response.status_code == 200, context.response.content
    assert 'access' in context.response.json(), context.response.content


@then("I should receive a 200 OK response with a list of events I have created")
def step_impl(context):

    # Ensure the response status is 200 OK
    assert context.response.status_code == 200, context.response.content

    # Parse the response content to retrieve the list of events
    response_data = context.response.json()
    assert isinstance(response_data, list), context.response.content

    # Get the primary key of the authenticated user
    user_id = context.user.id

    # Iterate through the list of events and check the creator of each event
    for event in response_data:
        assert event['created_by'] == user_id, f"Event created by {event['created_by']} instead of {user_id}"


@then('The response should contain "{message}"')
def step_impl(context, message):
    response_data = context.response.json()
    assert message in response_data, f"Expected '{message}' to be in response, but got '{error_message}'"

