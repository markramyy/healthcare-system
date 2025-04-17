@echo off

echo "Dropping database..."
python manage.py drop_db

echo "Making migrations..."
python manage.py makemigrations

echo "Migrating..."
python manage.py migrate

echo "Loading mock data..."
python manage.py load_mock

echo "Running server..."
python manage.py runserver
