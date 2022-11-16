
# Default configuration
SHELL     := /bin/bash
PYTHON    := python3
PIP       := ${PYTHON} -m pip
LINTER    := pycodestyle
FORMATTER := black
MAKE_TAG  := --no-print-directory

# Virtual env
VENV_NAME = venv


.PHONY: echo-cyan, echo-purple, echo-green, requirements, lint, format, clean


## Create virtualenv
venv:
	@$(MAKE) $(MAKE_TAG) echo-cyan msg="Creating and seting up a virtualenv..."
	@$(PYTHON) -m venv $(VENV_NAME)
	@. $(VENV_NAME)/bin/activate; \
	$(PIP) install --upgrade pip; \
	$(PIP) install -r requirements.txt
	@$(MAKE) $(MAKE_TAG) echo-green msg="Virtual created environment successfully ! ✨"
	@echo
	@echo "To activate it, please run 'source venv/bin/activate'"

## Update requirements.txt file
requirements: venv
	@rm requirements.txt 2> /dev/null
	@. venv/bin/activate; \
	$(PIP) freeze > requirements.txt
	@echo "$@.txt updated! ✨\n"

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

