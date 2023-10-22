# Event app

Event management app.Users can create,edit and register to events

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install and how to install them.

- django
- djangorestframework
- rest_framework_swagger
- drf-yasg
- behave-django
   
### Installing

A step by step series of examples that tell you how to get a development environment running.

1. Clone the repository:
```bash
git clone https://github.com/radupaunescu2021/django2.git

Navigate to the project directory:
cd django

Install the required dependencies:

pip install -r requirements.txt

Apply migrations:

python3.9 manage.py migrate

Run the server:

python3.9 manage.py runserver


### Usage


### User Creation

1. To create a new user, send a POST request to `/api/users/` with the following payload:

```json
{
    "username": "newuser",
    "password": "newpass"
}

Example using curl:

curl -X POST -H "Content-Type: application/json" \
     -d '{"username":"newuser", "password":"newpass"}' \
     http://localhost:8000/api/users/

### User Login and Authentication
To log in and obtain a token, send a POST request to /api/token/ with your credentials:
{
    "username": "newuser",
    "password": "newpass"
}

Example using curl:

curl -X POST -H "Content-Type: application/json" \
     -d '{"username":"newuser", "password":"newpass"}' \
     http://localhost:8000/api/token/

### Event Creation
To create a new event, send a POST request to /api/events/ with the event data:

{
    "name": "Test Event",
    "description": "Test Description",
    "start_date": "2023-11-25T10:00:00Z",
    "end_date": "2023-11-25T18:00:00Z",
    "capacity": 50
}

Example using curl with the token obtained during login:

curl -X POST -H "Content-Type: application/json" \
     -H "Authorization: Bearer <your_token>" \
     -d '{"name":"Test Event", "description":"Test Description", "start_date":"2023-11-25T10:00:00Z", "end_date":"2023-11-25T18:00:00Z", "capacity":50}' \
     http://localhost:8000/api/events/


### Event Registration

To register for an event, send a POST request to /api/events/<event_id>/register/:

Example using curl with the token obtained during login:

curl -X POST -H "Authorization: Bearer <your_token>" \
     http://localhost:8000/api/events/1/register/


To unregister from an event, send a DELETE request to the same endpoint.

Example using curl with the token obtained during login:

curl -X DELETE -H "Authorization: Bearer <your_token>" \
     http://localhost:8000/api/events/1/register/


### Filtering Events by Type

The API provides the ability to filter events based on their type. This is achieved through the use of the `event_type` query parameter on the relevant endpoints.

### Usage:

To filter events by a specific type, you can append the `event_type` query parameter to the endpoint URL, followed by the desired event type.

Example:

```http
GET /api/events/?event_type=MUSIC
This request will return all events of type 'Music'.

Available Event Types:
MUSIC
SPORT
POLITICS

Example Request using cURL:
curl -X GET "http://localhost:8000/api/events/?event_type=Music" -H "accept: application/json"


### Running the Tests
Tests have been created using BEHAVE BDD Framework

python3.9 manage.py behave -i event_management.feature
python3.9 manage.py behave


## API Documentation (or Exploring the API)

This project utilizes Swagger for API documentation and interactive exploration of the API. Swagger provides a user-friendly interface to send requests to the API and view responses, without the need to write code or use tools like `curl`.

### Accessing Swagger UI

1. Ensure your Django application is running, typically at `http://localhost:8000` if running locally.
2. Open your web browser and navigate to `http://localhost:8000/swagger/` (adjust the URL to match your deployment if not running locally).
3. The Swagger UI will load, displaying a list of all available API endpoints along with their methods, parameters, and responses.

### Using Swagger UI

1. **Authentication**: 
   - If an endpoint requires authentication, click on the "Authorize" button at the top-right corner of the Swagger UI.
   - Enter your credentials and click "Authorize" to obtain a token.
   - The token will be used for subsequent requests that require authentication.
   
2. **Sending Requests**:
   - Click on an endpoint to expand it, revealing the details of the endpoint.
   - Enter any required parameters, and click "Try it out" to send a request to the endpoint.
   - The request's response will be displayed below, including the status code, response body, and headers.

3. **Viewing Documentation**:
   - Click on an endpoint to view detailed documentation including the endpoint's purpose, parameters, and response format.
   - Use the documentation to understand the expected inputs and outputs for each endpoint.

This setup provides a straightforward way to interact with and understand the API, making it easier to integrate with or test the functionality of the application.

