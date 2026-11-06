.PHONY: install test lint format-check check clean

install:
	python -m pip install -e '.[dev]'

test:
	pytest

lint:
	ruff check .

format-check:
	ruff format --check .

check: test lint format-check

clean:
	rm -rf .pytest_cache .ruff_cache build dist *.egg-info
