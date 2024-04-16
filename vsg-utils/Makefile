PROJECT_NAME = vsg_utils

clean:
	@rm -rfv build/ dist/ *.egg-info
	@find . -iname "*.pyc" | xargs --no-run-if-empty rm -rfv
	@rm -fv .coverage*
	@rm -rfv .pytest_cache test-results htmlcov
	@find . -iname "__pycache__" -type d | xargs --no-run-if-empty rm -rfv
	@rm -rfv .tox
	@pip uninstall -y $(PROJECT_NAME)

install:
	poetry install --only main -v
