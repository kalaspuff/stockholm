.PHONY: test version tests build dist release
ifndef VERBOSE
.SILENT:
endif

default:
	@echo "Usage:"
	@echo "- make test         | run tests"
	@echo "- make version      | update versions"
	@echo "- make build        | build package"
	@echo "- make release      | upload dist and push tag"

pytest:
	poetry run pytest --cov-report term-missing --cov=stockholm tests/

flake8:
	poetry run flake8 stockholm/ tests/

mypy:
	poetry run mypy stockholm/

version:
	poetry version `python stockholm/__version__.py`

black:
	poetry run black -l 120 stockholm/ tests/

build:
	rm -rf dist/
	poetry build

release:
	make pytest
	make flake8
	make mypy
	make version
	make build
	poetry publish
	git add pyproject.toml stockholm/__version__.py
	git commit -m "Bumped version" --allow-empty
	git tag -a `python stockholm/__version__.py` -m `python stockholm/__version__.py`
	git push
	git push --tags

test: pytest flake8 mypy
tests: test
dist: build

