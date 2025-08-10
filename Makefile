.PHONY: dev lint fmt type test seed

dev:
	poetry run uvicorn main:app --reload

lint:
	poetry run ruff check .

fmt:
	poetry run ruff format .

type:
	poetry run mypy .

test:
	poetry run pytest tests/ -v

test-unit:
	poetry run pytest tests/unit/ -v

test-e2e:
	poetry run pytest tests/e2e/ -v



seed:
	python -m usersnack.scripts.seed_from_data
