# Makefile at <saiki/>
# ====================
# @saiki
# Last update: 2025-06-22
# -----------------------

# Main makefile for the project.
# By default, attempts running the backend.

.PHONY: build run-backend run-django migrate



# Environment variables
# ---------------------

ifeq ($(OS),Windows_NT)
define PYTHON
	python
endef
else
define PYTHON
	python3
endef
endif



# Building
# --------

# (currently empty)
build:



# Derivations
# -----------

-include .install.mak
-include src/backend/Makefile
