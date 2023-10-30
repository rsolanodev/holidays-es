check:
	poetry run black --check --diff .
	poetry run ruff check .
	poetry run mypy .

format:
	poetry run ruff check --fix .
	poetry run black .
