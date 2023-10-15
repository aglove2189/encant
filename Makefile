env:
	python -m venv venv
	./venv/bin/pip install .[dev]
	./venv/bin/pip uninstall encant -y
	./venv/bin/pre-commit install
