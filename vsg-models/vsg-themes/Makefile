PROJECT_NAME = vsg_themes

clean:
	@rm -rfv poetry.lock build/ dist/ *.egg-info
	@find . -iname "*.pyc" | xargs --no-run-if-empty rm -rfv
	@rm -fv .coverage*
	@rm -rfv .pytest_cache test-results htmlcov
	@find . -iname "__pycache__" -type d | xargs --no-run-if-empty rm -rfv
	@rm -rfv .tox
	@pip uninstall -y $(PROJECT_NAME)

dev-dependencies:
	pip install poetry==1.8.2
	pip install tox~=4.11

dependencies:
	pip install poetry==1.8.2

install: dependencies
	POETRY_VIRTUALENVS_CREATE=false	poetry install --no-cache --only main -v
	python -m nltk.downloader wordnet
	python -m nltk.downloader stopwords
	python -m nltk.downloader punkt

install-dev: dependencies
	POETRY_VIRTUALENVS_CREATE=false	poetry install --with dev -v
	python -m nltk.downloader wordnet
	python -m nltk.downloader stopwords
	python -m nltk.downloader punkt

# Tox will take care of all the remaining dependencies, so there's no need to include them here to prevent installing
# the project twice.
test: dev-dependencies
	tox
	python ../../test-standalone-utils/scrap_coverage.py --coverage-html-path './htmlcov/index.html' --readme-path 'README.md'

