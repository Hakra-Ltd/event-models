VENV := poetry run

lint: mypy ruff black
lint-fix: ruff-fix black-fix

# Linters
black:
	$(VENV) black --check event_models

black-fix:
	$(VENV) black event_models

ruff:
	$(VENV) ruff check event_models

ruff-fix:
	$(VENV) ruff check --fix event_models

mypy:
	$(VENV) mypy event_models

test:
	$(VENV) pytest -vvv

test-failed:
	$(VENV) pytest --last-failed -vvv;

