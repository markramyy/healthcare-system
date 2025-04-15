#!/bin/bash

python manage.py makemigrations
python manage.py migrate
python manage.py load_mock
python manage.py runserver
