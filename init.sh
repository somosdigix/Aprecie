#!/bin/bash
set -e

# echo "Starting SSH..."
# service ssh start

python /src/manage.py makemigrations
python /src/manage.py migrate
python /src/manage.py runserver 0.0.0.0:8000