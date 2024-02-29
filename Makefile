
VENV = .venv

CODE = \
    admin \
    api \
    db

JOBS ?= 4

makemigrations:
	poetry run alembic revision --autogenerate

migrate:
	poetry run alembic upgrade head

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

run_admin:
	poetry run python -m admin.run_admin

run_celery:
	celery -A api.tasks.tasks worker --loglevel=info --logfile=celery.log

run_celery_windows:
	poetry run celery -A api.tasks.tasks worker --loglevel=info --logfile=celery.log --pool=solo

run_celery_beat:
	celery -A api/tasks/tasks beat

run_api:
	poetry run uvicorn api.run_api:app --host 127.0.0.1 --port 8000

run_api_prod:
	gunicorn api/run_api:app --workers 4 --preload --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000

run_admin_prod:
	gunicorn admin/run_admin:app --workers 4 --preload --bind=0.0.0.0:5000