install:
	uv sync
	
build:
	./build.sh

local-start:
	uv run manage.py runserver

lint:
	uv run ruff check

lint-with-fix:
	uv run ruff check --fix

test:
	uv run pytest

test-pytest-coverage:
	uv run pytest --cov=task_manager --cov-report xml --cov-report term-missing

check: test lint