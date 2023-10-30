# Phicius Test

## Installation Steps

1. *Clone GitHub repository*
2. *Running*
```bash
pip install -r requirements.txt

python manage.py makemigrations

python manage.py migrate

python manage.py runserver
```
3. Start Playing :)

## Game "Guide"
1. First of all, two users must be created, all views require authentication.
2. Create a new board.
3. Log in and out between accounts to play with circles or crosses depending on what user plays what.

*It was made like this, logging in and out since the idea of having a whole game in a single session came later, focus was onto the general objectives, although, the game works perfectly.*

On top of that, there are two API views with almost identical code, this was made in order to allow one of them to manage the game and the other for POSTMAN purposes, testing validations, messages, signals and stuff. Also, that specific view has the API documentation made with 'drf-yasg' in openapi format, check that out too.

### Without further ado, I hope hearing from you again. May the force be with you :)