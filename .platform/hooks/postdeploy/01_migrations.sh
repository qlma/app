#!/bin/bash

source /var/app/venv/*/bin/activate
cd /var/app/current

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput