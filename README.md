# pokeapi_crud

pokeapi_crud

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

License: MIT

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

-   To run application locally:

```bash
    export COMPOSE_FILE=local.yml
```


```bash
    docker compose up
```

-   To execute tests (make sure the local docker is running):


```bash
    docker compose run --rm python manage.py test
```


### Setting Up Your Users

-   To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

-   To create a **superuser account**, use this command:


```bash
    docker compose run --rm python manage.py createsuperuser
```


For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

```bash
    docker compose run --rm mypy pokeapi_crud
```

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:
```bash
    docker compose run --rm coverage run -m pytest
    docker compose run --rm coverage html
    open htmlcov/index.html
```
