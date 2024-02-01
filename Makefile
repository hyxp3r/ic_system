
VENV = .venv

CODE = \
    admin \
    api \
    db

JOBS ?= 4

makemigrations:
	alembic revision --autogenerate

migrate:
	alembic upgrade head

lint:
	$(VENV)/bin/black --check $(CODE)
	$(VENV)/bin/flake8 --jobs $(JOBS) --statistics $(CODE)
	$(VENV)/bin/mypy --config-file mypy.ini $(CODE)

pretty:
	$(VENV)/bin/black --target-version py311 --skip-string-normalization $(CODE)
	$(VENV)/bin/isort $(CODE)
	$(VENV)/bin/unify --in-place --recursive $(CODE)

lint_windows:
	$(VENV)/Scripts/black --check $(CODE)
	$(VENV)/Scripts/flake8 --jobs $(JOBS) --statistics $(CODE)

pretty_windows:
	$(VENV)/Scripts/black --target-version py311 --skip-string-normalization $(CODE)
	$(VENV)/Scripts/isort $(CODE)
	$(VENV)/Scripts/unify --in-place --recursive $(CODE)

run-admin:
	poetry run python -m admin.app