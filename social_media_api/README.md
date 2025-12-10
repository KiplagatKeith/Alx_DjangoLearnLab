# Social Media API

A Django REST Framework API with **token-based authentication** for user registration, login, and profile management.

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install django djangorestframework
Run migrations:

bash
Copy code
python manage.py makemigrations
python manage.py migrate
Create a superuser (optional):

bash
Copy code
python manage.py createsuperuser
Run the server:

bash
Copy code
python manage.py runserver
API Endpoints
Endpoint	Method	Description
/api/register/	POST	Register a new user. Returns token.
/api/login/	POST	Log in and get token.
/api/accounts/	GET/PUT	Retrieve/update your profile (token required).

Example: Register
json
Copy code
POST /api/register/
{
  "username": "keith",
  "email": "keith@example.com",
  "password": "securepassword"
}
Response:

json
Copy code
{
  "user_id": 1,
  "username": "keith",
  "token": "b0a9e7f7b8..."
}
Example: Login
json
Copy code
POST /api/login/
{
  "username": "keith",
  "password": "securepassword"
}
Response:

json
Copy code
{
  "user_id": 1,
  "username": "keith",
  "token": "b0a9e7f7b8..."
}
User Model
Accounts (custom user)

username, email, password (from AbstractUser)

bio: optional text

profile_picture: optional image

followers: many-to-many to self (non-symmetrical)

yaml
Copy code
