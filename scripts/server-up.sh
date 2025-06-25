#!/usr/bin/env bash

# <scripts/server-up.sh>
# Raises the server.


# abort upon errors
set -e


# Running the Django server
python3 src/backend/manage.py runserver

