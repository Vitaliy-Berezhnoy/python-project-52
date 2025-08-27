install:
	uv sync

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

lint:
	uv run ruff check --fix

dev:
	uv run manage.py runserver

migrations:
	uv run manage.py makemigrations
	uv run manage.py migrate