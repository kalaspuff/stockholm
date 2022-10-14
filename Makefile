.PHONY: test version tests build dist release
ifndef VERBOSE
.SILENT:
endif

PACKAGENAME := $(shell poetry version | awk {'print $$1'})

default:
	@echo "Usage:"
	@echo "- make test         | run tests"
	@echo "- make black        | run black -l 120"
	@echo "- make release      | upload dist and push tag"

install:
	poetry install -E protobuf

pytest:
	PYTHONPATH=. poetry run pytest --cov-report term-missing --cov=${PACKAGENAME}/ tests -v

flake8:
	poetry run flake8 ${PACKAGENAME}/ tests/

mypy:
	poetry run mypy ${PACKAGENAME}/ tests/types/ tests/examples/

version:
	poetry version `python ${PACKAGENAME}/__version__.py`

black:
	poetry run black ${PACKAGENAME}/ tests/

isort:
	poetry run isort ${PACKAGENAME}/ tests/

build:
	rm -rf dist/
	poetry build

release:
	make install
	make pytest
	make flake8
	make mypy
	make version
	make build
	twine upload dist/stockholm-`python stockholm/__version__.py`*
	git add pyproject.toml ${PACKAGENAME}/__version__.py CHANGELOG.md
	git commit -m "Bumped version" --allow-empty
	git tag -a `python ${PACKAGENAME}/__version__.py` -m `python ${PACKAGENAME}/__version__.py`
	git push
	git push --tags

test: pytest flake8 mypy
tests: test
dist: build
lint: flake8 mypy
pylint: flake8 mypy
