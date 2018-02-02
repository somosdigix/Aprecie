#!/bin/bash
set -e

# echo "Starting SSH..."
# service ssh start

echo "python /src/manage.py makemigrations"
python /src/manage.py makemigrations

echo "python /src/manage.py migrate"
python /src/manage.py migrate

echo "python /src/manage.py runserver 0.0.0.0:8000"
python /src/manage.py runserver 0.0.0.0:8000