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

collectstatic:
	uv run python3 manage.py collectstatic --no-input

migrate:
	uv run python3 manage.py migrate

makemessages:
	uv run django-admin makemessages -l ru --no-obsolete