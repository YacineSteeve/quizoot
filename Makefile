
# Default configuration
SHELL := /bin/bash
PYTHON := python3
PIP := ${PYTHON} -m pip
MAKE_TAG := --no-print-directory

# Virtual env
VENV_NAME = venv
VENV_ACTIVATE := . $(VENV_NAME)/bin/activate

## Create virtualenv
.PHONY: venv
venv:
	$(PYTHON) -m venv $(VENV_NAME)
	@$(MAKE) $(MAKE_TAG) venv-activate
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt


## Activate virtual env
.PHONY: venv-activate
venv-activate:
	@$(MAKE) $(MAKE_TAG) echo-cyan msg="Activating virtualenv..."
	$(VENV_ACTIVATE)


## echo with cyan font https://gist.github.com/iamnewton/8754917
echo-cyan:  
	@echo -e "\033[36m${msg}\033[39m"
.PHONY: echo-cyan


## echo with purple font https://gist.github.com/iamnewton/8754917
echo-purple:
	@echo -e "\033[35m${msg}\033[39m"
.PHONY: echo-purple

