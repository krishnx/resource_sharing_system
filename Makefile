.PHONY: help migrate runserver test lint

help:
	@echo "Makefile commands:"
	@echo "  migrate     - Apply database migrations"
	@echo "  runserver   - Run Django development server"
	@echo "  test       - Run unit tests"
	@echo "  lint        - Run flake8 linter"

migrate:
	python manage.py migrate

install:
	python -m pip install -r requirements.txt

runserver:
	python manage.py runserver

test:
	python manage.py test

lint:
	flake8
