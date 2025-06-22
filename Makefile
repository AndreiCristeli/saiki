# Makefile at <saiki/>
# ====================
# @saiki
# Last update: 2025-06-12
# -----------------------

# Main makefile for the project.
# By default, attempts running the backend.

.PHONY: build run-backend



# Running the server
# ------------------

# Running the server application
run-backend:
	uvicorn src.backend.main:app

# Building
# --------

# (currently empty)
build:


# Others
# ------

include .install.mak

