#!/bin/bash

docker-compose -f docker-compose.dev.yml run --rm web python manage.py drop_db
docker-compose -f docker-compose.dev.yml run --rm web python manage.py makemigrations
docker-compose -f docker-compose.dev.yml run --rm web python manage.py migrate
docker-compose -f docker-compose.dev.yml run --rm web python manage.py load_mock
docker-compose -f docker-compose.dev.yml run --rm web python manage.py load_mock_appointments
docker-compose -f docker-compose.dev.yml run --rm web python manage.py load_mock_ehr
docker-compose -f docker-compose.dev.yml up --build
