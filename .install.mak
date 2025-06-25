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

PYTHON_VENV_DIR				:= .venv/
PYTHON_REQ_PACKAGES		    := docs/req.txt
PYTHON_PIP_LOG              := temp/pip-install.log

ifeq ($(OS),Windows_NT)
PYTHON_PIP					:= $(PYTHON_VENV_DIR)Scripts/python.exe -m pip
PYTHON_ACTIVATE_SCRIPT		:= $(PYTHON_VENV_DIR)Scripts/activate

# for some unknown reason Windows's version won't work... @TODO: adapt
define PYTHON_PIP_INSTALL_CMD
	call /$(PYTHON_ACTIVATE_SCRIPT) && \
	$(PYTHON_PIP) install --require-virtualenv --quiet --no-input --log "$(PYTHON_PIP_LOG)" --requirement "$(PYTHON_REQ_PACKAGES)"
endef
else
PYTHON_PIP                  := pip
PYTHON_ACTIVATE_SCRIPT      := $(PYTHON_VENV_DIR)bin/activate

define PYTHON_PIP_INSTALL_CMD
	. ./$(PYTHON_ACTIVATE_SCRIPT); \
	$(PYTHON_PIP) install --require-virtualenv --quiet --no-input --log "$(PYTHON_PIP_LOG)" --requirement "$(PYTHON_REQ_PACKAGES)"
endef
endif



# Setting up VENV and installing the requirement packages.

__setup_python:
	@$(PYTHON) -m venv $    (PYTHON_VENV_DIR)
	@$(PYTHON_PIP_INSTALL_CMD)
#. pip --require-virtualenv --quiet --no-input --requirement "$(PYTHON_REQ_TXT)"
	@echo "Python is setup. Run the following to activate the venv:"
	@echo "./$(PYTHON_ACTIVATE_SCRIPT)"

