
# Default configuration
SHELL       := /bin/bash
PYTHON      := python3
PIP         := ${PYTHON} -m pip
LINTER      := pycodestyle
FORMATTER   := black
MAKE_TAG    := --no-print-directory

# Virtual env
VENV_NAME   := venv
VENV_PYTHON := ${VENV_NAME}/bin/${PYTHON}


.PHONY: echo-cyan, echo-purple, echo-green, requirements, lint, format, clean


## Create virtualenv
venv:
	@$(MAKE) $(MAKE_TAG) echo-cyan msg="Creating and setting up a virtualenv..."
	@$(PYTHON) -m venv $(VENV_NAME)
	@. $(VENV_NAME)/bin/activate;
	@$(MAKE) $(MAKE_TAG) echo-green msg="Virtual environment created successfully ! ✨"

## Update requirements.txt file
requirements: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@rm requirements.txt 2> /dev/null
	$(PIP) freeze > requirements.txt
	@$(MAKE) $(MAKE_TAG) echo-green msg="\n$@.txt updated! ✨\n"

migration:
	@$(VENV_PYTHON) manage.py makemigrations
	@$(VENV_PYTHON) manage.py migrate

serve-back:
	@$(VENV_PYTHON) manage.py runserver

## Linting and formatting
lint: venv
	@$(LINTER) .

format: venv
	@$(FORMATTER) .

## echo with different colors font https://gist.github.com/iamnewton/8754917
echo-cyan:
	@echo -e "\033[36m${msg}\033[39m"

echo-purple:
	@echo -e "\033[35m${msg}\033[39m"

echo-green:
	@echo -e "\033[32m${msg}\033[39m"


clean:
	@rm -r venv
