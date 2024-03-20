.PHONY: clean
clean:
	find . -depth -name '__pycache__' -type d -exec rm -rf '{}' \;
	find . -name '*.py[co]' -type f -delete
	rm -rf build dist *.egg-info

.PHONY: test
test:
	PYTHONPATH=. pytest

.PHONY: build
build: clean
	python -m build

.DEFAULT_GOAL :=
