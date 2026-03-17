#!/usr/bin/env bash

# Upgrade pip (optional but recommended)
python3 -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Collect static files
python3 manage.py collectstatic --noinput

# Apply migrations to create all tables, including main_project
python3 manage.py migrate --noinput