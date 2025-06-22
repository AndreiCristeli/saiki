# Makefile for installing the requirements
# for the project.
# ----------------------------------- 
# Last update: 18-06-25.
# (Draft...)

# Observations:
# - Currently, setup is Windows based...;
# - Assumes python is already installed.

.PHONY: install __install


install: __install
	@echo "Installation complete."


install: __setup_python



# Python
# ------

PYTHON						:= python
PYTHON_VENV_DIR				:= .venv/
PYTHON_PIP					:= $(PYTHON_VENV_DIR)Scripts/python.exe -m pip
PYTHON_ACTIVATE_SCRIPT		:= $(PYTHON_VENV_DIR)Scripts/activate
PYTHON_REQ_TXT				:= docs/req.txt


# Setting up VENV and installing the requirement packages.

__setup_python:
	$(PYTHON) -m venv $(PYTHON_VENV_DIR)
# for some unknown reason Windows's python's venv pip doesn't reck "-r" wtf
#./"$(PYTHON_ACTIVATE_SCRIPT)"
# ./$(PYTHON_PIP) --require-virtualenv --quiet --no-input --requirement "$(PYTHON_REQ_TXT)"
	echo "Python is setup. Run the following to activate the venv:"
	echo "./$(PYTHON_ACTIVATE_SCRIPT)"

