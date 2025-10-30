Project Structure Overview

After creating the Django project, several important files and directories are generated automatically. Here’s a brief explanation of the key components:

1. settings.py

This file contains the configuration for the entire Django project.
It includes settings such as:

Database connections

Installed applications

Middleware

Static files configuration

Debug mode and allowed hosts

Any project-wide behavior or environment setup is managed here.

2. urls.py

This file acts as the URL router or table of contents for your project.
It maps specific URL paths to the corresponding views, allowing Django to determine what content to display when a user visits a particular URL.

3. manage.py

This is a command-line utility for interacting with your Django project.
You can use it to:

Run the local development server

Create and apply database migrations

Manage apps and users

Run Django shell commands

Example usage:

python manage.py runserver
python manage.py makemigrations
python manage.py migrate
