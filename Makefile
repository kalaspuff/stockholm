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
	PYTHONPATH=. pytest tests/

flake8:
	flake8 stockholm/ tests/

mypy:
	PYTHONPATH=. mypy stockholm/ tests/

version:
	poetry version `python stockholm/__version__.py`

build:
	rm -rf dist/
	poetry build

release:
	twine upload dist/stockholm-`python stockholm/__version__.py`.tar.gz dist/stockholm-`python stockholm/__version__.py`-py*.whl

test: pytest flake8 mypy
tests: test
dist: release

