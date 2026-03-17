#!/bin/bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput