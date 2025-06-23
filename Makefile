# Makefile at <saiki/>
# ====================
# @saiki
# Last update: 2025-06-22
# -----------------------

# Main makefile for the project.
# By default, attempts running the backend.

.PHONY: build run-backend run-django migrate

# Running the server
# ------------------

# Running the FastAPI server application
run-backend:
	uvicorn src.backend.main:app

# Running the Django server
run-django:
	python3 src/backend/manage.py runserver

# Run migrations: makemigrations + migrate
migrate:
	python3 src/backend/manage.py makemigrations
	python3 src/backend/manage.py migrate

# Building
# --------

# (currently empty)
build:


# Others
# ------

include .install.mak