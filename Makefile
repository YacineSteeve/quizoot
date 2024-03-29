
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


.PHONY: echo-cyan, echo-purple, echo-green, json-schemas, seed, requirements, migrations, serve-back, lint, format, clean


## Create virtualenv
venv:
	@$(MAKE) $(MAKE_TAG) echo-cyan msg="Creating and setting up a virtualenv..."
	@$(PYTHON) -m venv $(VENV_NAME)
	@. $(VENV_NAME)/bin/activate; \
	$(PIP) install --upgrade pip; \
	$(PIP) install -r requirements.txt
	@$(MAKE) $(MAKE_TAG) echo-green msg="Virtual environment created successfully ! ✨"
	@echo
	@echo "To activate it, please run 'source venv/bin/activate'"

## Update requirements.txt file
requirements: venv
	@. $(VENV_NAME)/bin/activate; \
	$(PIP) install -r requirements.txt; \
	@rm requirements.txt 2> /dev/null; \
	$(PIP) freeze > requirements.txt
	@$(MAKE) $(MAKE_TAG) echo-green msg="\n$@.txt updated! ✨\n"

json-schemas:
	@yarn --cwd ./interfaces/ run gen-schemas

seed:
	@$(VENV_PYTHON) manage.py seed

migrations:
	@$(VENV_PYTHON) manage.py makemigrations
	@$(VENV_PYTHON) manage.py migrate

serve-back:
	@$(VENV_PYTHON) manage.py runserver

## Linting and formatting
lint-back: venv
	@$(MAKE) $(MAKE_TAG) echo-cyan msg="\nLinting backend code..."
	@$(LINTER) . && $(MAKE) $(MAKE_TAG) echo-green msg="Backend code is clean ! ✨"

lint-front:
	@$(MAKE) $(MAKE_TAG) echo-cyan msg="\nLinting frontend code..."
	@yarn --cwd ./frontend/ run lint && $(MAKE) $(MAKE_TAG) echo-green msg="Frontend code is clean ! ✨"

lint: lint-back lint-front

format-back: venv
	@$(MAKE) $(MAKE_TAG) echo-cyan msg="\nFormatting backend code..."
	@$(FORMATTER) . && $(MAKE) $(MAKE_TAG) echo-green msg="Backend code is formatted ! ✨"

format-front:
	@$(MAKE) $(MAKE_TAG) echo-cyan msg="\nFormatting frontend code..."
	@yarn --cwd ./frontend/ run format && $(MAKE) $(MAKE_TAG) echo-green msg="Frontend code is formatted ! ✨"

format-interface:
	@$(MAKE) $(MAKE_TAG) echo-cyan msg="\nFormatting interface code..."
	@yarn --cwd ./interfaces/ run format && $(MAKE) $(MAKE_TAG) echo-green msg="Interface code is formatted ! ✨"

format: format-back format-front format-interface

## echo with different colors font https://gist.github.com/iamnewton/8754917
echo-cyan:
	@echo -e "\033[36m${msg}\033[39m"

echo-purple:
	@echo -e "\033[35m${msg}\033[39m"

echo-green:
	@echo -e "\033[32m${msg}\033[39m"


clean:
	@rm -r venv
